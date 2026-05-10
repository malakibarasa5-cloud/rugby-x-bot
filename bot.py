import os
import tweepy
import openai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Twitter/X API
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Debug: Print if secrets are loaded
print(f"OpenAI API Key loaded: {bool(openai.api_key)}")
print(f"Twitter Bearer Token loaded: {bool(TWITTER_BEARER_TOKEN)}")
print(f"Twitter API Key loaded: {bool(TWITTER_API_KEY)}")

def generate_rugby_content():
    """Generate AI-powered rugby content"""
    try:
        print("Attempting to generate content with OpenAI...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a rugby enthusiast and sports journalist. Generate engaging, entertaining rugby content for Twitter/X. Keep it under 280 characters. Include emojis and relevant hashtags."
                },
                {
                    "role": "user",
                    "content": "Generate a tweet about rugby tips, techniques, or interesting rugby facts."
                }
            ],
            temperature=0.7,
            max_tokens=100
        )
        content = response.choices[0].message.content.strip()
        print(f"Content generated successfully: {content}")
        return content[:280]  # Ensure it fits in a tweet
    except Exception as e:
        print(f"ERROR generating content: {type(e).__name__}: {e}")
        return None

def post_to_twitter(content):
    """Post content to Twitter/X"""
    try:
        print("Attempting to authenticate with Twitter API...")
        # Authenticate with Twitter API v2
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        print("Creating tweet...")
        # Post the tweet
        response = client.create_tweet(text=content)
        print(f"✅ Tweet posted successfully! Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"ERROR posting to Twitter: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the bot"""
    print(f"[{datetime.now()}] Rugby X Bot started")
    
    # Generate content
    print("Generating rugby content...")
    content = generate_rugby_content()
    
    if content:
        print(f"Generated content: {content}")
        print("Posting to Twitter/X...")
        success = post_to_twitter(content)
        if success:
            print("✅ Bot cycle completed successfully!")
        else:
            print("❌ Failed to post tweet")
    else:
        print("❌ Failed to generate content")

if __name__ == "__main__":
    main()
