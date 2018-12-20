from functools import lru_cache
import requests


@lru_cache(maxsize=10)
def get_tlds():
    """
    Gets the list of all public TLD suffix from https://publicsuffix.org/list/public_suffix_list.dat
    
    For more details on parsing visit https://publicsuffix.org/list/
    """
    tlds = set()
    resp = requests.get('https://publicsuffix.org/list/public_suffix_list.dat')
    for line in resp.text.split("\n"):
        if not line.startswith('//') and not line == None:
            tlds.add(line)
    return tlds

class InvalidDomain(Exception):
    """
    Exception raised when no TLD is matched with the domain.
    """

    def __init__(self, domain):
        self.domain = domain
    
    def __str__(self):
        return f"Domain '{self.domain}' did not match any TLD"


class TLDParserTree:

    def __init__(self):
        # fetch tlds and create the tree
        self.tlds = get_tlds()
        self._tlds_tree = {}
        self._exceptions = set()
        self._build_tlds_tree()

    def _build_tlds_tree(self):
        """
        Builds a TLDS tree using python dict for all the Top Level Domains.
        """
        for tld in self.tlds:
            if tld.startswith('!'):
                self._exceptions.add(tld.replace('!', ''))
            root = self._tlds_tree
            for part in reversed(tld.split('.')):
                new_root = root.get(part, None)
                if new_root == None:
                    new_root = {}
                    root[part] = new_root
                root = new_root
    
    def split_tld(self, domain):
        """
        Splits the domain into name and the TLD.

        :param domain: Domain to split. (Should not be a complete url, only the netloc is accepted)
        :return: A 2-tuple containing domain name and TLD
        """
        tld = []
        domain_parts = domain.split('.')
        # First check for the exception domains
        if domain in self._exceptions:
            return domain_parts[0], '.'.join(domain_parts[1:])
        sub = self._tlds_tree
        while domain_parts and not sub == {}:
            part = domain_parts.pop()
            next_sub = sub.get(part, None)
            if next_sub == None:
                # check for *. If found then this part is included in TLD
                # If not found then this domain part is in name
                more_required = sub.get('*', None)
                if more_required == None:
                    sub = {}
                    domain_parts.append(part)
                    continue
                next_sub = {}
            tld.insert(0, part)
            sub = next_sub
        
        if not len(tld):
            raise InvalidDomain(domain)
        return '.'.join(domain_parts), '.'.join(tld)

    def s(self, domain):
        """
        An alias to the split_tld method.
        """
        return self.split_tld(domain)