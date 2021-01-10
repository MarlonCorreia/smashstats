from graphqlclient import GraphQLClient
from dotenv import load_dotenv
load_dotenv()

import requests
import os
import json

class API():
    
    def __init__(self):
        self.client = GraphQLClient('https://api.smash.gg/gql/alpha')
        self.client.inject_token('Bearer ' + os.getenv("TOKEN"))

    def query_set_by_id(self, setId):
        result = self.client.execute('''
        query SetsByID($setId: ID!) {
            set(id: $setId) {
                displayScore
                    games {
                        winnerId
                        selections{
                            selectionValue
                                entrant {
                                    id
                                    name
                                }
                        }
                    }
            }
        }
        ''',
        {
        "setId": setId
        })

        return result

    def query_sets_in_event(self, event_id, page_number):
        result = self.client.execute('''
        query SetsInEvent($eventId: ID!, $page: Int!){
			event(id: $eventId) {
			  sets(
				page: $page
				perPage: 200
				sortType: STANDARD
			  ) {
				pageInfo {
				  total
				}
				nodes {
				  id
				}
			  }
	        }
        }    
        ''',
        {
            "eventId": event_id,
            "page": page_number

        })
        
        return result