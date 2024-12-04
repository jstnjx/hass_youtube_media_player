# YouTube Media Player Integration for Home Assistant

This custom integration for Home Assistant creates a media player entity that dynamically displays the media title, artist, and thumbnail from YouTube based on the state of a user-defined media player entity.
Features

Automatically updates media title, artist, and thumbnail when the user-defined media player is playing YouTube content.
Sets the media player state to idle when the source is not YouTube.

## Installation

1. Download the Integration: Clone or download this repository.

2. Copy to Home Assistant: Place the youtube_media_player folder into the custom_components directory in your Home Assistant configuration folder. If the folder doesn’t exist, create it.
    
        custom_components/      
        └── youtube_media_player/     
            ├── __init__.py        
            ├── config_flow.py            
            ├── const.py            
            ├── media_player.py            
            └── manifest.json

3. Restart Home Assistant: Restart your Home Assistant instance to recognize the new integration.

4. Add the Integration:
    Go to Settings > Devices & Services > Add Integration.
    Search for "YouTube Thumbnail Media Player."
    Configure the integration by selecting a media player entity and entering your YouTube API key.

5. Enjoy: A new media player entity will be created with dynamic YouTube metadata and thumbnails.

## Configuration Options

##### During setup, you will need to provide:

###### Media Player Entity:
Select an existing media player entity (e.g., a Chromecast or other supported device) whose state will be monitored.
###### YouTube API Key:
Obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).

## Usage

The integration-created media player entity will dynamically update its state, title, artist, and thumbnail whenever the user-defined media player entity is playing content from YouTube.
If the source is not YouTube, the media player state will change to idle.

## Troubleshooting

##### Invalid API Key:
If the API key is invalid, the media player will display "Error 403" as the media title and "API KEY RATE LIMIT REACHED" as the artist.
Verify the API key and ensure YouTube Data API v3 is enabled in the Google Cloud Console.

##### No Media Player Entity Created:
Ensure you have properly configured the integration and restarted Home Assistant after installation.
Check logs for any errors under Settings > System > Logs.

##### Missing Thumbnails:
Thumbnails depend on the YouTube API. If the thumbnail does not appear, ensure your API key has sufficient quota. 

#### Limitations:
Since the integration grabs the title and artist reported by the media player entity and uses the YouTube Data API v3 to search YouTube for this specific query it is not 100% guaranteed that it grabs the right thumbnail.
From my testing it worked everytime but never say never.

## Contributions

Contributions, suggestions, and bug reports are welcome! Please submit them via the Issues tab on this repository.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/jstnjx/hass_youtube_media_player?tab=MIT-1-ov-file) file for details.
