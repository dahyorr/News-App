 # News App
 Application created using Django


## Management commands
__get_items__


fetch last 100 news items from api
```bash
python manage.py get_items
```
## API Endpoints
GET: /api/news - Gets all news items

GET: /api/news/:id - Gets news item by id

GET: /api/story - Gets by news of type 'story'

GET: /api/story/:id - Gets by news of type 'story' by id

POST: /api/story/:id - Creates news of type 'story' by id

PUT: /api/story/:id - Update news of type 'story' by id

DELETE: /api/story/:id - Delete news of type 'story' by id

GET: /api/job/:id - Gets by news of type 'job' by id

POST: /api/job/:id - Creates news of type 'job' by id

PUT: /api/job/:id - Update news of type 'job' by id

DELETE: /api/job/:id - Delete news of type 'job' by id