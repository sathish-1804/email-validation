import re
import dns.resolver
import smtplib
import requests
import threading
import queue
import dns.reversename

CACHE_TTL = 600

# Initialize a DNS resolver with caching enabled
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8']
resolver.cache = dns.resolver.Cache()


# def is_valid_email(email):
#     # Check if "@" is present in the email
#     if "@" not in email:
#         return False

#     local_part, domain_part = email.split('@')

#     # Check for consecutive dots, hyphens, or underscores in the local part
#     if re.search(r'\.{2}|-{2}|_{2}', local_part):
#         return False

#     # Check for consecutive dots, hyphens, or underscores in the domain part
#     if re.search(r'\.{2}|-{2}|_{2}', domain_part):
#         return False

#     # Check for two consecutive dots, hyphens, or underscores anywhere in the email
#     if re.search(r'\.\-|\-\.|\.\.|\_\-|\-\_|\_\_|\.\.|--', email):
#         return False

#     # Validate email syntax
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None

def is_valid_email(email):
    # Comprehensive regex for email validation
    pattern = r'''
        ^                         # Start of string
        (?!.*[._%+-]{2})          # No consecutive special characters
        [a-zA-Z0-9._%+-]{1,64}    # Local part: allowed characters and length limit
        (?<![._%+-])              # No special characters at the end of local part
        @                         # "@" symbol
        [a-zA-Z0-9.-]+            # Domain part: allowed characters
        (?<![.-])                 # No special characters at the end of domain
        \.[a-zA-Z]{2,}$           # Top-level domain with minimum 2 characters
    '''
    
    # Match the entire email against the pattern
    return re.match(pattern, email, re.VERBOSE) is not None

# mx record validation
# Set the cache TTL (in seconds)

def query_dns(record_type, domain):
    try:
        # Try to resolve the record from cache first
        record_name = domain if record_type == 'MX' else f'{domain}.'
        cache_result = resolver.cache.get((record_name, record_type))
        if cache_result is not None and (dns.resolver.mtime() - cache_result.time) < CACHE_TTL:
            return True

        # Otherwise, perform a fresh DNS query
        resolver.timeout = 2
        resolver.lifetime = 2
        resolver.resolve(record_name, record_type)
        return True
    except dns.resolver.NXDOMAIN:
        # The domain does not exist
        return False
    except dns.resolver.NoAnswer:
        # No record of the requested type was found
        return False
    except dns.resolver.Timeout:
        # The query timed out
        return False
    except:
        # An unexpected error occurred
        return False


def has_valid_mx_record(domain):
    # Define a function to handle each DNS query in a separate thread
    def query_mx(results_queue):
        results_queue.put(query_dns('MX', domain))

    def query_a(results_queue):
        results_queue.put(query_dns('A', domain))

    # Start multiple threads to query the MX and A records simultaneously
    mx_queue = queue.Queue()
    a_queue = queue.Queue()
    mx_thread = threading.Thread(target=query_mx, args=(mx_queue,))
    a_thread = threading.Thread(target=query_a, args=(a_queue,))
    mx_thread.start()
    a_thread.start()

    # Wait for both threads to finish and retrieve the results from the queues
    mx_thread.join()
    a_thread.join()
    mx_result = mx_queue.get()
    a_result = a_queue.get()

    return mx_result or a_result


# smtp connection
def verify_email(email):
    # Split the email address into username and domain parts
    domain = email.split('@')[1]

    # Check the domain MX records
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NoAnswer:
        return False

    # Connect to the SMTP server and perform the email verification
    for mx in mx_records:
        try:
            smtp_server = smtplib.SMTP(str(mx.exchange))
            smtp_server.ehlo()
            smtp_server.mail('')
            code, message = smtp_server.rcpt(str(email))
            smtp_server.quit()
            if code == 250:
                return True
        except:
            pass

    return False


# temporary domain
def is_disposable(domain):
    blacklists = [
        'https://raw.githubusercontent.com/andreis/disposable-email-domains/master/domains.txt',
        'https://raw.githubusercontent.com/wesbos/burner-email-providers/master/emails.txt'
    ]

    for blacklist_url in blacklists:
        try:
            blacklist = set(requests.get(blacklist_url).text.strip().split('\n'))
            if domain in blacklist:
                return True
        except Exception as e:
            print(f'Error loading blacklist {blacklist_url}: {e}')
    return False
