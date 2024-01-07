import discord  , requests , random , httpx
from datetime import datetime
from discord.ext import commands

class Instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bio = None
        self.name = None
        self.username = None
        self.password = None
        self.email = None
        self.target = None
        self.Sessionid = None
        self.attempts = None

    def checker(self) :
        with open('proxies.txt' , 'r') as file :
            proxies=file.readlines()
        proxy_rl = f"http://{random.choice(proxies)}"
        proxy_username = "tpfocsiy"
        proxy_password="z8scv7l8rsv9"
        url = f"https://www.instagram.com/{self.target}/"
        response = httpx.get(url=url , proxies={"http" : proxy_rl } , auth=(proxy_username, proxy_password)).text
        get = "Instagram photos and videos"
        if get in response :
            return 'TAKEN'
        else :
            return 'A/B'
        
    def claimer(self) :
        url = 'https://www.instagram.com/api/v1/web/accounts/edit/'
        co = requests.get('https://instagram.com').cookies
        csrf = co.get('csrftoken')
        headers = {
        'X-Csrftoken': f'{csrf}',
        'Cookie': f"ig_did=29F806F6-618B-4AEE-AB10-3135FEFC0ADF; ig_nrcb=1; mid=ZKiWsQALAAHpZUSVh1zhvRB_rjKw; datr=r5aoZPJ_i4dQ4KOxwb85x848; oo=v1; csrftoken={csrf};dpr=1.25; sessionid={self.Sessionid};"
    }
        bio = self.bio
        name = self.name
        email = self.email
        phone = '' 
        target = self.target
        dat  = { 
        'first_name': name, 
        'chaining_enabled': "on",
        "email" : f'{email}',
        "biography": bio ,
        "username" : target ,
        'phone_number' :''
        }
        r =requests.post(headers=headers , data=dat ,url=url)
        if r.status_code == 200:
            return "claim"
        else :
            return f"{r}"
        
    def login(self):
        time = int(datetime.now().timestamp())
        url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
        payload = {'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'optIntoOneTap': 'false',
            'queryParams': {},
            'username': {self.username}}
        files=[

        ]
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        global csrf
        global sid
        csrf=response.cookies["csrftoken"]
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'X-Csrftoken': f'{csrf}',
            'Cookie': f"csrftoken={csrf}; mid=ZIrEtgALAAE7GrCUwQ9wcQbbrefW; ig_did=80445D30-C9F9-4D3F-8BF0-78B39275775C; ig_nrcb=1; datr=tcSKZFMeDkyjVKNghYr_9-WI"
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.json())
        x = response.json()
        if x["status"]=="ok" and x["authenticated"]!=None and x["authenticated"]==True:
            sid = response.cookies['sessionid']
            print(sid)
            self.Sessionid = sid
            return sid
        else :
            return "NO"    
        
    @commands.slash_command(name='sethelp' , description="Information about settings")
    @commands.is_owner()
    async def information(self , ctx):
        await ctx.response.send_message("Please Send info as this in this command **setsetting**\n```target:username:password:email:bio:name```")
    @commands.slash_command(name="setsetting" , description="Set setting of auto")
    @commands.is_owner()
    async def setsetting(self,interaction:discord.Interaction , j) :
        info = j.split(':')
        self.target = info[0]
        self.username = info[1]
        self.password=info[2]
        self.email=info[3]
        self.bio=info[4]
        self.name=info[5]
        await interaction.response.send_message(content="`Settings are saved`" , ephemeral=True)
    @commands.slash_command(name="deletesettings" , description="delete all settings")
    @commands.is_owner()
    async def deletesettings(self,ctx) :
        self.target = None
        self.username = None
        self.password=None
        self.email=None
        self.bio=None
        self.name=None
        await ctx.response.send_message(content="`settings was been deleted`" , ephemeral=True)

    @commands.slash_command(name="seesettings" , description="see saved settings")
    @commands.is_owner()
    async def setting(self,interaction:discord.Interaction) :
        if self.name is None :
            return await interaction.response.send_message(content="You don't have any saved" , ephemeral=True)
        user = self.username
        password = self.password
        email = self.email
        target = self.target
        embed = discord.Embed(title="Settings" , description=f"Username : {user}\nPassword : ||{password}||\nEmail : ||{email}||\nTarget : {target}" , color=discord.Color.random())
        await interaction.response.send_message(embed=embed , ephemeral=True)

    @commands.command(name="runauto" , description="Run auto")
    @commands.is_owner()
    async def runauto(self , ctx):
        if self.name is None :
            await ctx.send(content="Please check your setting" , ephemeral=True)
            return
        attempts = 0
        one = await ctx.send("EGO-AUTO IS RUNNING ...")
        checker = self.checker()
        if checker.startswith('A/B') :
            await one.edit(content=f"**@{self.target}** is available")
            logger = self.login()
            if logger.startswith('NO') :
                await one.edit(content="log in is failed check")
            else :
                claimer = self.claimer()
                if claimer.startswith('claim') :
                    embed = discord.Embed(title="EGO-VI" , description="This is so easy @[{}](https://instagram.com/{})".format(self.target,self.target) , color=discord.Color.brand_red())
                    await one.delete()
                    await ctx.send(embed=embed)
                    return
                else :
                    await one.delete()
                    embed = discord.Embed(title="EGO-VI" , color=discord.Color.magenta()).add_field(name='Error' ,value=f"```{claimer}```")
                    await ctx.send(embed=embed)
                    return
        else :
            two = await ctx.send(f"@{self.target} Starting EGO-VI ...")
            monitor = self.checker()
            while monitor.startswith('TAKEN') :
                monitori = self.checker()
                if monitori.startswith('A/B') :
                    await two.edit(content=f"**@{self.target}** is available")
                    logger = self.login()
                    if logger.startswith('NO') :
                        await two.edit(content="log in is failed check")
                    else :
                        claimer = self.claimer()
                        if claimer.startswith('claim') :
                            embed = discord.Embed(title="EGO-VI" , description="This is so easy @[{}](https://instagram.com/{}) \nAt : {}".format(self.target,self.target , attempts) , color=discord.Color.brand_red())
                            await two.delete()
                            await ctx.send(embed=embed)
                            return
                        else :
                            await two.delete()
                            embed = discord.Embed(title="EGO-VI" , color=discord.Color.magenta()).add_field(name='Error' ,value=f"```{claimer}```")
                            await ctx.send(embed=embed)
                            return
                else :
                    attempts +=1
                    await two.edit(content=f'@{self.target} attempts > {attempts}')
                    print(attempts)
                    
def setup(bot):
    bot.add_cog(Instagram(bot))
