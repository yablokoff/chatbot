__author__ = 'yablokoff'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from bot.models import Tweet


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import tweepy

        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET_KEY)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        public_tweets = tweepy.Cursor(api.user_timeline, id='milonovinfo').items(4000)
        for tweet in public_tweets:
            if Tweet.objects.filter(id_str=tweet.id_str).exists():
                continue
            else:
                new_tweet = Tweet.objects.create(
                    id_str=tweet.id_str,
                    text=tweet.text,
                    created_at=tweet.created_at
                )
                new_tweet.save()
                self.stdout.write(self.style.SUCCESS(u'Added tweet {} ({}): {} '.format(
                    tweet.id_str,
                    tweet.created_at,
                    tweet.text))
                )