from faker import Faker

faker = Faker()


def random_valid_dns_name() -> str:
    return faker.domain_word()


def random_valid_dns_ttl() -> int:
    return faker.random_int(min=1, max=604800)


def random_ipv4_address() -> str:
    return faker.ipv4(True)


def random_ipv6_address() -> str:
    return faker.ipv6(True)
