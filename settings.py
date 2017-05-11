# Let's just use the local mongod instance. Edit as needed.

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
#MONGO_HOST = 'localhost'
#MONGO_PORT = 27017
#MONGO_USERNAME = 'user'
#MONGO_PASSWORD = 'user'

RESOURCE_METHODS = ['GET','POST','DELETE']
ITEM_METHODS = ['GET','PATCH','DELETE']
URL_PREFIX = 'api'
MONGO_DBNAME = 'scrapping'
DOMAIN = {
    'behanceUsers': {
        "schema" : {
            "_id" : {'type' : 'string'},
        	"profileDisplayName" : {'type' : 'string'},
        	"appreciationsCount" : {'type' : 'string'},
        	"followersCount" : {'type' : 'string'},
        	"projectViewsCount" : {'type' : 'string'},
        	"profileLocation" : {'type' : 'string'},
        	"behanceURL" : {'type' : 'string'},
        	"profileWebsite" : {'type' : 'string'},
        	"resumeUrl" : {'type' : 'string'},
        	"lasteUpdated" : {'type' : 'date'},
        	"fields" : {'type' : 'string'},
        	"followingCount" : {'type' : 'string'},
        	"profileCompany" : {'type' : 'string'},
        	"emails" : {'type' : 'string'},
        	"profileTitle" : {'type' : 'string'}
        }
    },
'users': {
        'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'username',
            },
        'schema': {
            'firstname': {
                'type': 'string'
            },
            'lastname': {
                'type': 'string'
            },
            'username': {
                'type': 'string',
		        'unique': True
            },
    	    'password': {
    		      'type': 'string'
    	    },
            'phone': {
                'type': 'string'
            }
        }
    }
}
