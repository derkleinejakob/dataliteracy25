

### Translation
- send_translation_requests.py: To avoid Gemini's rate limits, translation is sent in batches of varying sizes, retrying with a smaller batch size after failure. This is semi-automatic so that once no requests are possible anymore due to rate limits, one has to restart later at the point of last successful iteration. 
- process_translations.py: Once all requests are sent, load and process the model's responses and create a new dataframe with the translated speeches