def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('login', help='Authenticate user')
    p.set_defaults(func=execute)

def execute(args, parser):
    from .auth import authorize
    authorize()
