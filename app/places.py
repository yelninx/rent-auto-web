from flask import request, redirect, render_template
from flask_login import login_required, current_user
from requests import get, put, post
from forms.places import EditPlaceForm


def add_places_routes(app):
    @app.route('/places')
    @login_required
    def places():
        places_ = get('http://localhost:8080/api/v2/places').json()['places']
        return render_template('places.html', places=places_)

    @app.route('/places/<int:place_id>', methods=['GET', 'POST'])
    @login_required
    def edit_places(place_id):
        place = get(f'http://localhost:8080/api/v2/places/{place_id}').json()['places']
        if current_user.is_admin:
            form = EditPlaceForm()
            if request.method == 'GET':
                form.name.data = place['name']
                form.owner_id.data = place['owner_id']
                form.address.data = place['address']
            if form.validate_on_submit():
                place_update = put(f'http://localhost:8080/api/v2/places/{place_id}',
                                   json={'name': form.name.data, 'owner_id': form.owner_id.data,
                                         'address': form.address.data}).json()
                if 'success' in place_update:
                    return redirect('/')
                else:
                    return render_template('edit_place.html', form=form, message=place_update)
            return render_template('edit_place.html', form=form)

    @app.route('/add/places', methods=['GET', 'POST'])
    @login_required
    def add_place():
        if current_user.is_admin:
            form = EditPlaceForm()
            if form.validate_on_submit():
                place_add = post('http://localhost:8080/api/v2/places',
                                 json={'name': form.name.data, 'owner_id': form.owner_id.data,
                                       'address': form.address.data}).json()
                if 'success' in place_add:
                    return redirect('/')
                else:
                    return render_template('edit_place.html', form=form, message=place_add)
            return render_template('edit_place.html', form=form)
