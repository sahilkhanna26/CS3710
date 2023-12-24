# Fuzzer skeleton code

import aiohttp, asyncio, args

async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    wordfile = open(args.wordlist, "r")
    data = args.data
    extensions = args.extensions
    headers_1 = args.headers
    match_codes = args.match_codes
    header_dict = {}
    if(len(headers_1)>0):
        for header in headers_1:
            h_list = header.split(':')
            clean_list = []
            for h in h_list:
                k = h.strip()
                clean_list.append(k)
            header_dict[clean_list[0]] = clean_list[1]



    method = args.method
    method= method.strip()
    init_url = args.url
    substring_url = init_url[0:len(init_url) - 4]


    words = []
    for x in wordfile:
        x = x.strip()
        words.append(x)

    async with aiohttp.ClientSession() as session:
        for word in words:
            new_url = substring_url + word
            url_list = []
            url_list.append(new_url)
            if(len(extensions)!= 0):
                for extension in extensions:
                    e_url = new_url+extension
                    url_list.append(e_url)

            # print(new_url)
        # asynchronous loading of a URL:
            if(len(extensions)==0):
                async with session.request(method = method,url=new_url, data=data, headers = header_dict) as response:
                    await response.text()
                    if(response.status in match_codes):
                        print(response.status, new_url)

            elif(len(extensions)!=0):
                for i in url_list:
                    async with session.request(method = method,url=i, data=data, headers = header_dict) as response:
                        await response.text()
                        if(response.status in match_codes):
                            print(response.status, i)







# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    asyncio.run(fuzz(arguments))
