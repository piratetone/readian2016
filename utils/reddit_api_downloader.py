from pprint import pprint #pip install pprint
import praw # pip install praw
user_agent = 'Readian political 0.0 bias detector by /u/piratetone'
reddit_connection = praw.Reddit(user_agent=user_agent)
from praw.errors import HTTPException
import json


def get_comment_tree(comment_gen,keyword,submission_obj):
    '''
    Recursive method to get all comments and all replies within a given
    Comment object

    takes in a comment iterator, a keyword to indicate which level of replies we
    are at, and the orginal Submission object to refresh and get more comments
    in the case that we run into a MoreComments object

    return list of comments and their respective replies in a flat list
    '''
    ret_lst = []
    for comment in comment_gen:
        if isinstance(comment,praw.objects.MoreComments):
            submission_obj.replace_more_comments(limit=None)
        else:
            print keyword,' type ',type(comment)
            print keyword,' Obj ',comment
            print keyword,' fullname ',comment.fullname
            print keyword,' Body ',comment.body

            comment_dict = { #format comments will be stored in for our own internal purposes
            'fullname':comment.fullname,
            'body':comment.body,
            'keyword':keyword
            }
            ret_lst.append(comment_dict) # append comment to returned list
            if comment.replies: # if comments exist step down another level in the tree, else return the list to then be extended into the original list
                print keyword,' Replies ',comment.replies
                replies_keyword = 'Replies 1'
                if keyword != 'Comments':
                    keyword_split = keyword.split()
                    replies_keyword = ' '.join([keyword_split[0],str(int(keyword_split[1])+1)]) # add 1 to indicate how many levels of replies we are away from original comment
                ret_lst.extend(get_comment_tree(comment.replies,replies_keyword,submission_obj))
        return ret_lst


def get_all_subreddit_data(subreddit_name):
    '''
    Returns all comments and posts for a given subreddit in the form
    {Submission_fullname : [list of comments/replies] }
    '''

    ret_dict = {} # post : [comments]

    try:
        subreddit_obj = reddit_connection.get_subreddit(subreddit_name)
    except HTTPException:
        print 'Name not found\n' #Currently unknown what happens if you actually put in a non existent name, this is just my guess as to what would happen
        return None
    content_gen = subreddit_obj.get_top(limit=None) # make limit None, to get all posts
    for submission in content_gen:
        print 'Submission obj ',submission
        print 'Submission fullname ',submission.fullname
        ret_dict[submission.fullname] = get_comment_tree(submission.comments,'Comments',submission)

    return ret_dict

def get_subreddits(subreddits):
    '''
    Takes names of subreddits and appends all the data to a json file under
    data called subreddit_data.json

    NOTE: Json formatting may not currently be how we want it to be, will
    adjust in the future
    '''
    with open('data/subreddit_data.json','a') as json_write: #may need to change filename in local env
        for subreddit_name in subreddits:
            subreddit_data = get_all_subreddit_data(subreddit_name)
            print 'Printing out data for the subreddit',subreddit_name
            pprint(subreddit_data)
            json.dump(subreddit_data,json_write,sort_keys=True, indent=4)

subreddits = ['The_Donald']
get_subreddits(subreddits)
