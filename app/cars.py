from flask import request, redirect, render_template
from flask_login import login_required, current_user
from requests import get, put, post, delete
from werkzeug.utils import secure_filename

from forms.cars import EditCarForm


def add_car_routes(app):
    @app.route('/cars/<int:car_id>', methods=['GET', 'POST'])
    @login_required
    def edit_cars(car_id):
        car = get(f'http://localhost:8080/api/v2/cars/{car_id}').json()['cars']
        if current_user.is_admin:
            form = EditCarForm()
            if request.method == 'GET':
                form.model.data = car['model']
                form.brand.data = car['brand']
                form.place_id.data = car['place_id']
                form.is_taken.data = car['is_taken']
                form.year.data = car['year']
                form.image.data = car['image']
            if form.validate_on_submit():
                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save('../static/images/' + filename)
                else:
                    filename = car['image']
                car_update = put(f'http://localhost:8080/api/v2/cars/{car_id}',
                                 json={'model': form.model.data, 'brand': form.brand.data,
                                       'place_id': form.place_id.data,
                                       'is_taken': 'true' if form.is_taken.data in ['True', '1'] else 'false',
                                       'year': form.year.data, 'image': filename}).json()
                if 'success' in car_update:
                    return redirect('/')
                else:
                    return render_template('edit_car.html', form=form, message=car_update)
            return render_template('edit_car.html', form=form)
        else:
            car_update = put(f'http://localhost:8080/api/v2/cars/{car_id}',
                             json={'model': car['model'], 'brand': car['brand'], 'place_id': car['place_id'],
                                   'year': car['year'], 'image': car['image'], 'is_taken': 'true'}).json()
            if 'success' in car_update:
                return redirect('/')
            else:
                return render_template('index.html', message=car_update)

    @app.route('/add/cars', methods=['GET', 'POST'])
    @login_required
    def add_car():
        if current_user.is_admin:
            form = EditCarForm()
            if form.validate_on_submit():
                if form.image.data:
                    filename = secure_filename(form.image.data.filename)
                    form.image.data.save('../static/images/' + filename)
                else:
                    filename = 'default.png'
                car_add = post(f'http://localhost:8080/api/v2/cars',
                                 json={'model': form.model.data, 'brand': form.brand.data,
                                       'place_id': form.place_id.data,
                                       'is_taken': 'true' if form.is_taken.data in ['True', '1'] else 'false',
                                       'year': form.year.data, 'image': str(filename)}).json()
                if 'success' in car_add:
                    return redirect('/')
                else:
                    return render_template('edit_car.html', form=form, message=car_add)
            return render_template('edit_car.html', form=form)

    @app.route('/delete/cars/<int:car_id>', methods=['GET', 'POST'])
    @login_required
    def delete_car(car_id):
        if current_user.is_admin:
            car_delete = delete(f'http://localhost:8080/api/v2/cars/{car_id}')
            if 'success' in car_delete:
                return redirect('/')
        return redirect('/')