import os
from reddchat import create_app

app = create_app()
print([
    rule
    for rule in app.url_map.iter_rules()
])


def main():
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
    except Exception as e:
        print(f'Error starting server: {e}')


if __name__ == '__main__':
    main()
