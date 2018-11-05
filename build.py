from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import subprocess
from git import *
from shutil import copyfile


TOKEN = "bot token"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# to do - use a configuration file
roms = {'lineage': (("git://github.com/LineageOS/android.git", "lineage-16.0"), '/root/kektreasure/lineage', 1)}
devices = {'land': [['https://github.com/RiteshSaxena/android_device_xiaomi_land', 'device/xiaomi/land', 'lineage-15.1'], ['https://github.com/RiteshSaxena/android_kernel_xiaomi_msm8937', 'kernel/xiaomi/msm8937', 'lineage-15.1'], ['https://github.com/RiteshSaxena/proprietary_vendor_xiaomi', 'vendor/xiaomi', 'lineage-15.1-land']]}
allowed = [298452985]


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("I am just another buildbot! /help to check the list of available commands!")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("availabe commands - /build <rom name> <device> <build type> <clean - optional>")


@dp.message_handler(commands=['build'])
async def build(message: types.Message):
    def clone(link, directory, br):
        repo = Repo.clone_from(
            link, roms[arglist[0]][1]+'/'+directory,
            branch=br
        )
    args = message.get_full_command()
    arglist = args[1].split()
    user = message.from_user.id
    if user in allowed:
        await message.reply('building {} for {}, type- {}'.format(arglist[0], arglist[1], arglist[2]))
        if arglist[0] in roms:
            if os.path.exists(roms[arglist[0]][1]):
                await message.reply('seems like {} is already synced!'.format(arglist[0]))
                romexist = 1
            else:
                await message.reply('syncing {}'.format(arglist[0]))
                os.makedirs(roms[arglist[0]][1])
                repoinit = subprocess.Popen(['repo', 'init', '-u', roms[arglist[0]][0][0], '-b', roms[arglist[0]][0][1]], cwd=roms[arglist[0]][1])
                repoinit.wait()
                reposync = subprocess.Popen(['repo', 'sync'], cwd=roms[arglist[0]][1])
                reposync.wait()
                romexist = 1
        else:
            await message.reply('rom is not available for building yet!')
            romexist = 0
            devicecl = 0
        if romexist:
            if arglist[1] in devices:
                for i in range(0, len(devices[arglist[1]])):
                    if os.path.isdir(roms[arglist[0]][1]+'/'+devices[arglist[1]][i][1]):
                        await message.reply('{} found! not cloning it'.format(devices[arglist[1]][i][1]))
                        devicecl = 1
                    else:
                        await message.reply('{} not found! cloning it'.format(devices[arglist[1]][i][1]))
                        clone(*devices[arglist[1]][i])
                        devicecl = 1
            else:
                await message.reply('device is not available for building yet!')
                devicecl = 0
        if arglist[2] not in ('eng', 'userdebug', 'user'):
            await message.reply('build type incorrect! stopping build')
            devicecl = 0
        if devicecl:
            if roms[arglist[0]][2] == 1:
                await message.reply('seems like the rom has brunch! using eet')
                copyfile('builder.sh', roms[arglist[0]][1]+'/builder.sh')
                if len(arglist) == 4 and arglist[3] == 'clean':
                    compile = subprocess.Popen(['/bin/bash', 'builder.sh', arglist[0]+'_'+arglist[1]+'-'+arglist[2], 'clean'], cwd=roms[arglist[0]][1])
                else:
                    compile = subprocess.Popen(['/bin/bash', 'builder.sh', arglist[0]+'_'+arglist[1]+'-'+arglist[2]], cwd=roms[arglist[0]][1])
            elif roms[arglist[0]][2] != 1:
                await message.reply('using custom command!')
                copyfile('builder.sh', 'builder1.sh')
                with open("builder1.sh", "r") as initshell:
                    buf = initshell.readlines()

                with open("builder1.sh", "w") as finalshell:
                    for line in buf:
                        if line == "#!/bin/bash\n":
                            line = line + "jabbcmd={}\n".format(roms[arglist[0]][2])
                        finalshell.write(line)
                copyfile('builder1.sh', roms[arglist[0]][1]+'/builder.sh')
                if len(arglist) == 4 and arglist[3] == 'clean':
                    compile = subprocess.Popen(['/bin/bash', 'builder.sh', arglist[0]+'_'+arglist[1]+'-'+arglist[2], 'custom', 'clean'], cwd=roms[arglist[0]][1])
                else:
                    compile = subprocess.Popen(['/bin/bash', 'builder.sh', arglist[0]+'_'+arglist[1]+'-'+arglist[2], 'custom'], cwd=roms[arglist[0]][1])

            if os.path.isfile('{}/log.txt'.format(roms[arglist[0]][1])):
                os.remove('{}/log.txt'.format(roms[arglist[0]][1]))

            compile.wait()
            try:
                # to do - make this statement more secure (see drawbacks\of shell=True on google)
                romzip = subprocess.check_output('ls out/target/product/'+arglist[1]+'/'+arglist[0]+'*'+'-'+arglist[1], cwd=roms[arglist[0]][1], shell=True)
            except subprocess.CalledProcessError:
                romzip = 'arbitiaryfile.lmfaoxdd'
            if os.path.isfile(romzip):
                # to do - process the gdrive output and send the link, replace os.system with subprocess
                os.system('gdrive upload {}/out/target/product/{}/{}'.format(roms[arglist[0]][1], arglist[1], romzip))
                await message.reply('uploaded to gdrive! check your drive')
            else:
                # to do - process the gdrive output and send the link, replace os.system with subprocess
                os.chdir(roms[arglist[0]][1])
                os.system('gdrive upload {}'.format(roms[arglist[0]][1]+'/log.txt'))
                await message.reply('got error! log uploaded to gdrive! check eet. If it says completed, then navigate to rom dir manualy and upload')

    else:
        await message.reply('bish you are not in the allowed list')


if __name__ == '__main__':
    executor.start_polling(dp)
