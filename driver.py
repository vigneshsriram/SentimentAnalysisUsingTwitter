import sys, codecs
import ConfigParser

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got


class driver():
    def fetch_tweets(self,configfile):
        Config = ConfigParser.ConfigParser()
        Config.read(configfile)
        companies=Config.sections()

        for company in companies:
            username = Config.get(company,'username')
            since = Config.get(company, 'since')
            until = Config.get(company, 'until')
            querysearch = Config.get(company, 'querysearch')
            near = Config.get(company, 'near')
            within = Config.get(company, 'within')
            maxtweets = Config.get(company, 'maxtweets')
            toptweets = Config.get(company, 'toptweets')
            outputFileName = Config.get(company, 'output')

            tweetCriteria = got.manager.TweetCriteria().setUsername(username).\
                 setSince(since).setUntil(until).setQuerySearch(querysearch).\
                 setNear(near).setWithin(within).setMaxTweets(maxtweets).\
                 setTopTweets(toptweets)

            outputFile = codecs.open(outputFileName, "w+", "utf-8")

            outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

            def receiveBuffer(tweets):
                for t in tweets:
                    outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
                    t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                    t.hashtags, t.id, t.permalink)))
                outputFile.flush();
                print('%d more tweets saved on file...' % len(tweets))

            got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

def ConfigSectionMap(configfile,section):
    dict1={}
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    options = Config.options(section)

    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None

    return dict1


def main():
    configfile = sys.argv[1]
    d = driver()
    d.fetch_tweets(configfile)


main()