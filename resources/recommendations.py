from flask import jsonify, request
from flask_restful import Resource


from .recommender.retrieve_songs import features_from_url
from .recommender.content_based import get_recommended_artists
from .recommender.tm_concerts import get_concerts

# /artist routes

class RecommendationAPI(Resource):
    def get(self):
        try:
            body = request.json
            # Retrieving songs and their features from Spotify
            tracklist = features_from_url(body["elementURL"], body["limit"])
        except Exception as e:
            return {"Musics couldn't be found" : str(e)}
        
        # Getting recommended artists from the cosine similarity module
        recomm_artists = get_recommended_artists(tracklist)

        all_concerts = []
        
        # Setting an arbitrary limit if the number of recommended artists is greater than x
        limit = 15 if (len(recomm_artists) > 15) else len(recomm_artists)

        # We take only k recommended artists for practical and computational reasons
        for artist in recomm_artists[:limit]:
            print("Artiste : ", artist)
            
            # Adding concerts from current artist to the list of concerts
            all_concerts.extend(get_concerts(artist))
        
        if not all_concerts:
            return {"Sorry, we haven't found any concerts matching your suggested artists" : 200}
        
        # Returning concerts sorted by date (ascending)
        return jsonify(sorted(all_concerts, key=lambda x: x["date"]))


