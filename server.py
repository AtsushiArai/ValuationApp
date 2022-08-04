from valuation._init_ import app, db

db.init_app(app)
db.app = app

# if __name__ == '__main__':
#     app.run()

app.run()