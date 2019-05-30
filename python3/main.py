import flask
import logging
import sys
import os

from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure
from gumo.datastore.infrastructure import DatastoreRepositoryMixin


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

core_configure(
    google_cloud_project='levii-playground',
    google_cloud_location='asia-northeast1',
)

if 'DATASTORE_EMULATOR_HOST' in os.environ:
    datastore_configure(
        use_local_emulator=True,
        emulator_host=os.environ['DATASTORE_EMULATOR_HOST'],
    )
else:
    datastore_configure(
        use_local_emulator=False
    )


class SampleRepository(DatastoreRepositoryMixin):
    def save(self, name: str):
        entity = self.DatastoreEntity(key=self.datastore_client.key('Book'))

        embedded_entity = self.DatastoreEntity()
        embedded_entity.update({'entity_key': 'entity_value'})

        entity.update({
            'name': name,
            'embedded_json': {
                'json_key': 'value'
            },
            'embedded_entity': embedded_entity,
        })
        self.datastore_client.put(entity=entity)

    def fetch_all(self):
        query = self.datastore_client.query(kind='Book')

        return list(query.fetch())


@app.route('/')
def hello():
    results = SampleRepository().fetch_all()

    return flask.jsonify([
        str(book) for book in results
    ])


@app.route('/create')
def create():
    SampleRepository().save(name=flask.request.args.get('name', 'sample book'))

    return flask.jsonify({'done': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
