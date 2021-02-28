# spotify-analysis
Use the spotify streaming history I obtained from Spotify to analyze my listening habit. It is still in development, and I have only just finished getting the track features from the Spotify Web API with the python script `create_data.py`.
 
How the python script `create_data.py` works:
  1. Extract all the streaming history json files in the input directory.
  2. Since the streaming history comes without track IDs, the unique track IDs for all the tracks are retrieved by the search API. 
  The result is dumped to `streaming_history_with_track_id.json`.
  3. Retrieve the tracks features by the track API with the track IDs obtained from the last step.
  The result is dumped to `streaming_history_with_track_id_and_features.json`
  
Note:  
  1. `auth_info.json` is a template, please obtain your own Client ID and Client Secret from Spotify for Developers at https://developer.spotify.com/dashboard/, and then
  overwrite the strings in fields `client_id` and `client_secret`.
  Then select 'Edit Settings' in the same dashboard and whitelist (add) http://localhost:7777/callback in the redirect URIs.
  2. Please download your personal data from Spotify from your account dashboard at https://www.spotify.com/ in the privacy settings.
    This process might take a while, mine took about 5 days. After you get your personal data, make a directory `input` and copy the `StreamingHistory*.json` file(s) into the `input` directory. 
  3. Make a  `output` directory for storing json files created by the `create_data.py` python script.
