from flask import Flask
# from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# app.config['SECRET_KEY'] = ''
# app.config['SQLALCHEMY_DATABASE_URI'] = ''

# import nomadiq_app.image_scrape
# import nomadiq_app.poi_scrape
# import nomadiq_app.city_recommendation
# import nomadiq_app.keyword_recommendation
# import nomadiq_app.collaborative_filter
import nomadiq_app.routes


# this allows for us to run this with python
if __name__ == '__main__':
    app.run(debug=True)
