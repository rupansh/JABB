# JABB
Just Another Buildbot

**Usage** :- 

    python3.7 build.py

**Requirements** :-

aiogram

GitPython

# **How to configure** :

 - Install **python3.7** (3.5 , the default shipped with ubuntu won't work!)
 - Install **gdrive** (here's a nice tutorial -  https://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/ )
 - Install all the required dependencies for building a rom
 - Install the requirements using pip(or use the **requirements.txt**)
 - Put your bot token in the **TOKEN** variable inside quotes

***To add support for a rom :-***

 construct a **dictionary** with key : value as follows -  

     {'romname' : (('manifest url', 'manifest branch'), 'location to sync to from /', 1)}
   **important note**- don't add / to the ending of the path of the ROM!, the romname should be what u use with brunch (i.e brunch lineage_devicename. If i were to add lineage, i would keep romname as lineage!)
   
  *(ps. The quotes are important since the values have to be string type so are the parenthesis)*

  *(if the rom uses something other than brunch, put the command in place of the 1 inside double quotes. for example, the dictionary for carbon rom would look like -*

     carbon = {'carbon': (("https://github.com/CarbonROM/android.git", "cr-6.1"), '/home/build/carbon', 'make carbon -j8')}
)

 put this in any arbitrary variable(say xyz) (see variable assignment if you don't know how to on google)

 and then add this line below the 'roms' dictionary - 

     roms.update(xyz)

***adding a new device is slightly more time consuming.***

same like before, construct a **dictionary** like this - 

    {'devicename' : [['device tree link', 'device/yourvendor/devicename', 'branch'], ['kernel link', 'kernel/yourvendor/whatev', 'branch'], ['vendor link', 'vendor/yourvendor', 'branch]]}
   *(here, yourvendor is the manufacturer of your device.*)

again, put it in an arbitrary variable(say abc)

and update it! - 

    devices.update(abc)

***adding an allowed user-***

remove my userid from the allowed list. and replace it with yours! to add multiple users simply do this-

    allowed = [userid1, userid2, userid3]

*ps- you shouldn't use quotes this time!*
 
 # How to use it on telegram

    /build romname devicename buildtype(user or userdebug or eng) clean(optional)
    
   /help shows you the same but whatever
   
   using the clean option will run a clean build

# ToDo

- Use a configuration file instead of the mess

- Process Gdrive output and send a file link directly

- Display compilation progress

 
**Feel free to make PRs and Issues!**
