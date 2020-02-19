# -*- coding: utf-8 -*-

import os
import re
import sys
import chkdel
import signal
import random
import difflib
import mwclient
import requests
import pywayback
import savepagenow
import checkchannel
import time
from time import sleep
import datetime
from datetime import timedelta
import pywikibot
from pywikibot import config
from urllib.request import Request, urlopen
from termcolor import colored

TestFile = False # when not testing
site = mwclient.Site('commons.wikimedia.org')
fileslist = '/data/project/ytrb/master/FilesForReview.txt'
RegexOfLicenseReviewTemplate = r"{{(?:|\s*)[LlYy][IiOo][CcUu][EeTt][NnUu][SsBb][Ee](?:|\s*)[Rr][Ee][Vv][Ii][Ee][Ww](?:|\s*)(?:\|.*|)}}"
VimeoUrlPattern = re.compile(r'vimeo\.com\/((?:[0-9_]+))')
YouTubeUrlRegex = re.compile(r'https?\:\/\/(?:www|)(?:|\.)youtube\.com/watch\Wv\=([^\"&?\/ ]{11})')
FromVimeoRegex = re.compile(r'{{\s*?[Ff]rom\s[Vv]imeo\s*(?:\||\|1\=|\s*?)(?:\s*)(?:1\=|)(?:\s*?|)([0-9_]+)')
FromYouTubeRegex = re.compile(r'{{\s*?[Ff]rom\s[Yy]ou[Tt]ube\s*(?:\||\|1\=|\s*?)(?:\s*)(?:1|=\||)(?:=|)([^\"&?\/ ]{11})')
AllowedlicensesArray = ['by-sa', 'by', 'publicdomain', 'cc0']
StandardCreativeCommonsUrlRegex = re.compile('https\:\/\/creativecommons\.org\/licenses\/(.*?)\/(.*?)\/')

class Review:

    def __init__(
        self,
        page,
    ):
        self.page = page

    def informatdate(self):
        StandardDate = (datetime.datetime.now()+timedelta(0)).strftime('%Y-%m-%d')
        return StandardDate

    def random_line(self, fname):
        lines = open(fname).read().splitlines()
        try:
            return random.choice(lines)
        except IndexError:
            print("Start reviewing again",  file=open(fileslist, "a"))
            self.getfile()

    def get_file_size_in_bytes(self, file_path):
        if not os.path.exists(fileslist):
            with open(fileslist, 'w'): pass
            
        size = os.path.getsize(file_path)
        return size

    def uploader(self, filename, link=True):
        """user that uploaded the video"""
        page = pywikibot.Page(SITE, filename)
        history = page.getVersionHistory(reverse=True, total=1)
        if not history:
            return "Unknown"
        if link:
            return "[[User:%s|%s]]" % (history[0][2], history[0][2])
        else:
            return history[0][2]

    def OwnWork(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('{{own}}') != -1):
            return True
        elif (LowerCasePageText.find('own work') != -1):
            return True
        else:
            return False

    def getfile(self):
        file_path = fileslist
        size = self.get_file_size_in_bytes(file_path)
        print("\n")
        print(colored(" Current File size: %s " % size, 'yellow'))
        if 0 < size < 512:
            print(colored(" As only few files left, getting New Files  " , 'green'))
            category = site.categories['License_review_needed_(video)']
            for page in category:
                namefile = page.name
                print(namefile,  file=open(fileslist, "a"))
        try:
            filename = self.random_line("%s" % (fileslist))
        except UnicodeDecodeError:
            f = open(fileslist, 'w')
            f.close()
        with open("%s" % (fileslist), "r") as f:
            lines = f.readlines()
        with open("%s" % (fileslist), "w") as f:
            for line in lines:
                if line.strip("\n") != filename:
                    f.write(line)
        return filename

    def FlickrVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('flickr.com/photos') != -1):
            return True
        else:
            return False

    def VimeoVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('{{from vimeo') != -1):
            return True
        elif (LowerCasePageText.find('vimeo.com') != -1):
            return True
        else:
            return False

    def YouTubeVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('{{from youtube') != -1):
            return True
        elif (LowerCasePageText.find('youtube.com') != -1):
            return True
        else:
            return False

    def FacebookVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('www.facebook.com') != -1):
            return True
        else:
            return False

    def InternetArchiveVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('archive.org/details/') != -1):
            return True
        else:
            return False

    def TwitterVideo(self, pagetext):
        LowerCasePageText = pagetext.lower()
        if (LowerCasePageText.find('twitter.com') != -1):
            return True
        else:
            return False

    def reviewthefiles(self):
        if TestFile is False:
            file_link = self.getfile()
        else:
            file_link = TestFile
        try:
            file_page = pywikibot.Page(SITE, file_link)
        except ValueError:
            sleep(12)
            print(colored(" Exiting, Invalid file name " , 'red'))
            return
        old_text = file_page.get(get_redirect=True, force=True)
        print(colored(file_link, 'magenta'))
        filename = file_link
        page = site.pages[filename]
        pagetext = page.text()
        LowerCasePageText = pagetext.lower()

        if chkdel.check(pagetext) == True:return

        if self.OwnWork(pagetext) == True:
            print(filename, "is own work but marked for review")
            new_text = re.sub(RegexOfLicenseReviewTemplate, "" , old_text)
            EditSummary = "@%s Removing licenseReview Template, not required for ownwork." % self.uploader(filename,link=True)
            try:
                self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
            except pywikibot.LockedPage as error:
                print(colored("Page is locked '%s'." % error, 'red'))
                return

        if self.FlickrVideo(pagetext) == True and self.YouTubeVideo(pagetext) == False and self.VimeoVideo(pagetext) == False:
            print(filename, "is a video from flickr")
            new_text = re.sub(RegexOfLicenseReviewTemplate, "{{FlickrReview}}" , old_text)
            EditSummary = "@%s It's a video from  flickr, marking for flickr review, it should add this file to [[Category:Flickr videos review needed]]." % self.uploader(filename,link=True)
            try:
                self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
            except pywikibot.LockedPage as error:
                print(colored("Page is locked '%s'." % error, 'red'))
                return

        if self.VimeoVideo(pagetext) == True and self.YouTubeVideo(pagetext) == False and self.FlickrVideo(pagetext) == False:
            print(colored("It's a video from vimeo.com !" , 'white'))
            try:
                try:
                    matches = VimeoUrlPattern.finditer(pagetext)
                    for m in matches:
                        VimeoVideoId = (m.group(1))
                except:
                    print(colored("Cannot find Vimeo's video ID in vimeo url" , 'yellow'))
                try:
                    matches = FromVimeoRegex.finditer(pagetext)
                    for m in matches:
                        VimeoVideoId = (m.group(1))
                except:
                    print(colored("Cannot find Vimeo's video in From Vimeo template" , 'yellow'))

                OriginalURL = "https://vimeo.com/{video_id}".format(video_id=VimeoVideoId)

                video_id = VimeoVideoId

            except:
                print(colored("Cannot find Vimeo's video ID!" , 'red'))
                return
            archive_url = pywayback.check(OriginalURL)
            req = Request(archive_url,headers={'User-Agent': 'User:YouTubeReviewBot on wikimedia commons'})
            try:
                webpage = urlopen(req).read().decode('utf-8')
            except:
                   print(colored("WayBack Machine didn't returning page, but archived!" , 'red'))
                   return
            VimeoChannelIdRegex = r"http(?:s|)\:\/\/vimeo\.com\/(.{0,30})\/video"
            matches = re.finditer(VimeoChannelIdRegex, webpage, re.MULTILINE)
            for m in matches:
                VimeoChannelId = m.group(1)
            try:
                VimeoChannelId
            except NameError:
                print(colored("Channel ID not  found on vimeo webpage !" , 'red'))
                return
            if checkchannel.IsTrusted(VimeoChannelId) == True:pass
            if checkchannel.IsBad(VimeoChannelId) == True:return
            print(colored("Vimeo - searching for creativecommons.org" , 'yellow'))
            try:
                if re.search(r"creativecommons.org", webpage) is not None:
                    print(colored("Vimeo - creativecommons.org found" , 'green'))
                    matches = StandardCreativeCommonsUrlRegex.finditer(webpage)
                    for m in matches:
                        licensesP1 = (m.group(1))
                        licensesP2 = (m.group(2))
                    if any(licensesP1 in s for s in AllowedlicensesArray):
                        print(colored("Vimeo - licenses okay for commons" , 'green'))
                    else:
                        print(colored("Vimeo - not okay cc license" , 'red'))
                        return
                    new_text = re.sub(RegexOfLicenseReviewTemplate, "{{VimeoReview|id=%s|license=%s-%s|ChannelID=%s|archive=%s|date=%s}}" % (video_id, licensesP1, licensesP2, VimeoChannelId, archive_url, self.informatdate()), old_text)
                else:
                    print(colored("Vimeo - creativecommons.org NOT found" , 'red'))
            except Exception as e:
                print(e)
                print(colored("Exception while searching for Vimeo - creativecommons.org" , 'red'))
            try:
                new_text
            except Exception as e:
                print(e)
                return
            DetailsVimeo = "License review passed ", " Channel Name/ID:", VimeoChannelId, " Video ID:", video_id, " License :", licensesP1,"-",licensesP2, "Archived Video on WayBack Machine"
            EditSummary = "{0}".format(DetailsVimeo)
            try:
                self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
            except pywikibot.LockedPage as error:
                print(colored("Page is locked '%s'." % error, 'red'))
            return

        if self.YouTubeVideo(pagetext) == True and self.VimeoVideo(pagetext) == False and self.FlickrVideo(pagetext) == False:
            print(colored("It's a video from youtube.com !" , 'white'))
            # Get channel If from file page text
            try:
                try:
                    matches = YouTubeUrlRegex.finditer(pagetext)
                    for m in matches:
                        YouTubeVideoId = (m.group(1))
                except:
                    print(colored("Cannot find YouTube's video ID in youtube url" , 'yellow'))
                try:
                    matches = FromYouTubeRegex.finditer(pagetext)
                    for m in matches:
                        YouTubeVideoId = (m.group(1))
                        YouTubeVideoId = re.sub(r'\}', '', YouTubeVideoId)
                except:
                    print(colored("Cannot find YouTube's video ID in From YouTube template" , 'yellow'))
                OriginalURL = "https://www.youtube.com/watch?v={video_id}".format(video_id=YouTubeVideoId)
                video_id = YouTubeVideoId
            except:
                new_text = re.sub(RegexOfLicenseReviewTemplate, "{{YouTubeReview}}" , old_text)
                SummaryPart1 = "Hi, %s It's a video from YouTube as per my opinion algorithms, but" % self.uploader(filename,link=True)
                EditSummary = "%s I was unable to get video Id from this file page. Marking for YouTubeReview, it should help humans in reviewing your file faster." % SummaryPart1
 
                print(colored("Cannot find YouTube's video ID!" , 'red'))
                try:
                    self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
                except pywikibot.LockedPage as error:
                    print(colored("Page is locked '%s'." % error, 'red'))
                return
            # Reqest way back machine
            archive_url = pywayback.check(OriginalURL)
            req = Request(archive_url,headers={'User-Agent': 'User:YouTubeReviewBot on wikimedia commons'})
            try:
                webpage = urlopen(req).read().decode('utf-8')
            except:
                print(colored("WayBack Machine didn't returning page, but archived!" , 'red'))
                return
            VideoAvailableCheck = True
            if (webpage.find('YouTube account associated with this video has been terminated') != -1):
                VideoAvailableCheck = False
            if (webpage.find('playerErrorMessageRenderer') != -1):
                VideoAvailableCheck = False
            if (webpage.find('Video unavailable') != -1):
                VideoAvailableCheck = False
            if (webpage.find('If the owner of this video has granted you access') != -1):
                VideoAvailableCheck = False
            if (webpage.find('player-unavailable') != -1) and (webpage.find('Sorry about that') != -1):
                VideoAvailableCheck = False
            if VideoAvailableCheck == False:
                new_text = re.sub(RegexOfLicenseReviewTemplate, "{{YouTubeReview}}" , old_text)
                EditSummary = "Hey, @%s It's a video from YouTube as per my algorithms, but I failed to review it (Video not available). But I am marking with {{YouTubeReview}}, this should help humans quickly locate your file and review it." % self.uploader(filename,link=True)
                try:
                    self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
                except pywikibot.LockedPage as error:
                    print(colored("Page is locked '%s'." % error, 'red'))
                print(colored("### Video not available as per latest archive ###", 'red'))
                return
            else:
                pass

            # Some useful regexes
            YouTubeChannelIdRegex = r"data-channel-external-id=\"(.{0,30})\""
            YouTubeChannelIdRegex2 = r"[\"']externalChannelId[\"']:[\"']([a-zA-Z0-9_-]{0,25})[\"']"
            YouTubeChannelNameRegex1 = r"\\\",\\\"author\\\":\\\"(.{1,50})\\\",\\\""
            YouTubeChannelNameRegex2 = r"\"ownerChannelName\\\":\\\"(.{1,50})\\\","
            YouTubeVideoTitleRegex1 = r"\"title\":\"(.{1,160})\",\"length"
            YouTubeVideoTitleRegex2 = r"<title>(?:\s*|)(.{1,250})(?:\s*|)- YouTube(?:\s*|)</title>"

            # try to get channel Id
            try:
                try:
                    matches = re.finditer(YouTubeChannelIdRegex , webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeChannelId = m.group(1)
                except:
                    print("channel Id not found")
                try:
                    matches = re.finditer(YouTubeChannelIdRegex2, webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeChannelId = m.group(1)
                except:
                    print("channel Id not found")

            except Exception as e:
                print(e)
                print(colored("Channel ID not  found on webpage !" , 'red'))
                return

            # Try to Channel name
            try:
                try:
                    matches = re.finditer(YouTubeChannelNameRegex1, webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeChannelName = m.group(1)
                except:
                    print("YouTubeChannelName not found")
                try:
                    matches = re.finditer(YouTubeChannelNameRegex2, webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeChannelName = m.group(1) 
                except:
                    print("YouTubeChannelName not found")

            except Exception as e:
                print(e)
                print(colored("YouTube Channel Name not  found on webpage !" , 'red'))
                return

            # Try to get YouTube Video's Title
            try:
                try:
                    matches = re.finditer(YouTubeVideoTitleRegex1, webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeVideoTitle = m.group(1)
                except:
                    print("YouTube Video's Title not found")
                try:
                    matches = re.finditer(YouTubeVideoTitleRegex2, webpage, re.MULTILINE)
                    for m in matches:
                        YouTubeVideoTitle = m.group(1)
                except:
                    print("YouTube Video's Title not found")
            except Exception as e:
                print(e)
                print(colored("YouTube Video's Title NOT  found on webpage !" , 'red'))
                return

            print(YouTubeVideoTitle)
            YouTubeVideoTitle = re.sub(r'[{}\|\+\]\[]', r'-', YouTubeVideoTitle)

            # Clean shit, if present in Video tilte or Channel Name
            try:
                YouTubeChannelName
            except Exception as e:
                print(colored(e , 'red'))
                return

            YouTubeChannelName = re.sub(r'[{}\|\+\]\[]', r'-', YouTubeChannelName)
            
            print(
                colored(" YouTube video id:", "yellow"),colored(video_id, "green"),"\n",
                colored("Name of Channel :", "yellow"),colored(YouTubeChannelName, "green"),"\n",
                colored("Title of video :", "yellow"),colored(YouTubeVideoTitle, "green"),"\n",
                colored("Commons uploader :", "yellow"),colored(self.uploader(filename, link=False), "green"),"\n",
                colored("Archived link :", "yellow"),colored(archive_url, "white"),
                )

            try:
                TAGS = str(
                "{{YouTubeReview"
                "|id=" + video_id + 
                "|ChannelName=" + YouTubeChannelName + 
                "|ChannelID=" + YouTubeChannelId +
                "|title=" + YouTubeVideoTitle + 
                "|archive=" + archive_url +
                "|date=" + self.informatdate() +
                "}}"
                )
                print(TAGS)

            except:
                TAGS = ''
                print(colored("TAGS for YouTube couldnot be generated" , 'red'))

            if checkchannel.IsTrusted(YouTubeChannelId) == True:
                print("TrustedChannel found")
                TrustedChannel = True
            else:
                TrustedChannel = False

            if checkchannel.IsBad(YouTubeChannelId) == True:return


            if re.search(r"Creative Commons", webpage) is not None or TrustedChannel == True:
                new_text = re.sub(RegexOfLicenseReviewTemplate, TAGS, old_text)
            else:
                new_text = re.sub(RegexOfLicenseReviewTemplate, "{{YouTubeReview}}" , old_text)
                print(colored("Failed Review : Video is not Creative commons license and not from a trusted channel." , 'red'))
                SummaryPart1 = "Hi, %s this file's from YouTube as per my algorithms, but  I was not successful in reviewing this file (CC not found) but" % self.uploader(filename,link=True)
                EditSummary = "%s don't worry I am tagging it for {{YouTubeReview}}, this should result in a faster review by a human reviewer." % SummaryPart1
                try:
                    self.commit(old_text, new_text, file_page, "{0}".format(EditSummary))
                except pywikibot.LockedPage as error:
                    print(colored("Page is locked '%s'." % error, 'red'))
                return

            try:
                if new_text == old_text:
                    print(colored("No change in page, maybe already reviewed !" , 'white'))
                    if TestFile != False:
                        sys.exit(0)
                    else:
                        return
            except Exception as e:
                print(e)
                print(colored("NEW TEXT NOT DEFINED, CUZ CC TAG NOT FOUND IN WEBPAGE" , 'red'))
                return
            if TrustedChannel == True:
                try:
                    TrustTextAppend = "[[User:YouTubeReviewBot/Trusted|✔️ - Trusted YouTube Channel of  %s ]]" %  YouTubeChannelName
                    DetailsYouTube = TrustTextAppend, "License review passed ", " Title of video:", video_title, " Video ID:", video_id,  " UploadDateYoutube:", published_on, " Channel ID:", YouTubeChannelId, "Archived Video on WayBack Machine"
                except:
                    video_title = YouTubeVideoTitle
                    TrustTextAppend = "[[User:YouTubeReviewBot/Trusted|✔️ - Trusted YouTube Channel of  %s ]]" %  YouTubeChannelName
                    DetailsYouTube = TrustTextAppend, "License review passed", " Title of video:", video_title, "Channel Name:", YouTubeChannelName , " Video ID:", video_id,  " Channel ID:", YouTubeChannelId, "Archived Video on WayBack Machine"
                    EditSummary = "{0}".format(DetailsYouTube)
            elif TrustedChannel != True:
                try:
                    DetailsYouTube = "License review passed ","Channel Name:", YouTubeChannelName, " Title of video:", video_title, " Video ID:", video_id,  " UploadDateYoutube:", published_on, " Channel ID:", YouTubeChannelId, "Archived Video on WayBack Machine"
                except:
                    video_title = YouTubeVideoTitle
                    DetailsYouTube = "License review passed ", " Title of video:", video_title, "Channel Name:", YouTubeChannelName, " Video ID:", video_id,  " Channel ID:", YouTubeChannelId, "Archived Video on WayBack Machine"
                    EditSummary = "{0}".format(DetailsYouTube)
            else:
                print("No Edit Summary FOUND for YouTube")
            try:
                self.commit(
                    old_text, new_text, file_page, "{0}".format(EditSummary)
                )
            except pywikibot.LockedPage as error:
                print(colored("Page is locked '%s'." % error, 'red'))
            if TestFile != False:
                sys.exit(0)
            else:
                return

        if self.VimeoVideo(pagetext) == False and self.YouTubeVideo(pagetext) == False:
            print(colored("Video not supported, neither YouTube nor Vimeo" , 'red'))
            return
        
        else:return

    @staticmethod
    def commit(old_text, new_text, page, comment):
        if new_text == old_text:return
        print(colored("\n About to commit changes to: '%s'" % page.title() , 'green'))

        # Show the diff
        for line in difflib.context_diff(
            old_text.splitlines(1), new_text.splitlines(1)
        ):
            if line.startswith("+ "):
                print(colored(line , 'green'))
            elif line.startswith("- "):
                print(colored(line , 'red'))
            elif line.startswith("! "):
                print(colored(line , 'yellow'))
            else:
                print(line)


        print("\n")

        if SIMULATE:
            choice = "n"
        elif ALWAYS:
            choice = "y"
        else:
            question = "Do you want to accept these changes to '%s' with comment '%s' ? [y]es, [n]o and [q]uit" % (page.title(), comment)
            
            choice = pywikibot.input(question, password=False, default='q', force=False)

        if choice == "y":
            page.put(new_text, summary=comment, watch=True, minor=False)
        elif choice == "q":
            print(colored("Aborting" , 'red'))
            sys.exit(0)
        else:
            print(colored("Changes to '%s' ignored" % page.title() , 'yellow'))

def RunLicenseReview(check):
    candidates = []
    templates = list(range(1,600))
    for template in templates:
        candidates.append(Review(templates))
    for candidate in candidates:
        try:
            check(candidate)
        except pywikibot.NoPage as error:
            print(colored("No page found '%s'." % error, 'red'))
        except pywikibot.LockedPage as error:
            print(colored("Page is locked '%s'." % error, 'red'))
        if STOP:
            break

# Auto reply yes to all questions
ALWAYS = False
# Auto answer no
SIMULATE = False
# Flag that will be set to True if CTRL-C was pressed
STOP = False

def main(*args):
    global ALWAYS
    global SIMULATE
    global SITE

    worked = False
    Lreview = False

    # First look for arguments that should be set for all operations
    for arg in sys.argv[1:]:
        if arg == "-always":
            ALWAYS = True
            sys.argv.remove(arg)
            continue
        elif arg == "-silmulate":
            SIMULATE = True
            sys.argv.remove(arg)
            continue
        elif arg == "-review":
            Lreview = True
            sys.argv.remove(arg)
            continue
        elif arg == "-help":
            Lreview = True
            sys.argv.remove(arg)
            continue
        else:
            return

    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    # Abort on unknown arguments
    for arg in args:
        if arg not in [
            "-review",
            "-always",
            "-silmulate",
            "-help",
        ]:
            print(colored("Warning - unknown argument '%s' aborting, see -help." % arg, 'red'))
            sys.exit(0)

    for arg in args:
        worked = True
        if arg == "-review":
            if Lreview:
                print(colored("Retriving random file for license review !", 'blue'))
                RunLicenseReview(Review.reviewthefiles)

    if not worked:
        print(colored("Warning - specify an argument, see -help.", 'red'))

def signal_handler(signal):
    global STOP
    print("\n\nReceived SIGINT, aborting ...\n")
    STOP = True

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
