import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re




async def fetch_data(url,id, headers, session, dist,pattern):
    try:
        async with session.get(url + f"{id}", headers=headers, timeout=1800) as response:
            #Important shit
            response.raise_for_status()  # Raise an exception for HTTP errors
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('span', id="ctl00_cntphmaster_lblCourseCodeResult").text
            match = pattern.match(title)

            #Export Information 
            Ccode = match.group('code') if match != None else title
            Ctile = match.group('title')  if match != None else None
            Cch = match.group('credit_hours') if match != None else None

            CFaculity = soup.find('span',id='ctl00_cntphmaster_lblfac').text.replace("Faculty : ", "")
            CSchool = soup.find('span',id='ctl00_cntphmaster_lblDept').text.replace("School : ", "")

            CLecH_tag = soup.find('input',id="ctl00_cntphmaster_grdTeachingMethod_ctl02_txtTeachingMethodCreditHours")
            CTutH_tag = soup.find('input',id="ctl00_cntphmaster_grdTeachingMethod_ctl03_txtTeachingMethodCreditHours")
            CLabH_tag = soup.find('input',id="ctl00_cntphmaster_grdTeachingMethod_ctl04_txtTeachingMethodCreditHours")

            CLecH = CLecH_tag.get('value') if CLecH_tag != None else None
            CTutH = CTutH_tag.get('value') if CTutH_tag != None else None
            CLabH = CLabH_tag.get('value') if CLabH_tag != None else None


            CType = None

            if soup.find('input',id="ctl00_cntphmaster_rdbAsCodedegreeclass_0").has_attr("checked") :
                CType = "UG"
            elif soup.find('input',id="ctl00_cntphmaster_rdbAsCodedegreeclass_1").has_attr("checked") :
                CType = "PG"
            
            CEle = False
            if soup.find('input',id="ctl00_cntphmaster_chElective").has_attr("checked") :
                CEle = True
            


            #Write to the csv file
            dist.write(f"{id},\"{Ccode}\",\"{Ctile}\",{Cch},\"{CFaculity}\",\"{CSchool}\",{CLecH},{CTutH},{CLabH},\"{CType}\",{CEle}\n")

            print(f"{id} Found.")

    except asyncio.TimeoutError:
        print(f"TimeoutError for {url + f'{id}'}")
        with open('Timeout-IDs.txt','a') as file:
            file.write(f"{id}\n")
        

    except Exception as e:
        #print(f"{id} was not found.")
        print(id," : ",e)
        with open('Failed-IDs.txt','a') as file:
            file.write(f"{id}\n")
        

async def main():
    url = "https://sis.ejust.edu.eg/UI/ED_COURSE/EntCoursePackageDtls.aspx?type=10&EdCourseId="

    headers = {
            'authority': 'sis.ejust.edu.eg',
            'Cookie': '#Insert your cookie here :)',

    }

    pattern = re.compile(r'(?P<code>\w+)-(?P<title>.*?)\s\((?P<credit_hours>\d+)\sCH\)')

    with open('final.csv', 'a') as dist:
        # Create an aiohttp session
        async with aiohttp.ClientSession() as session:
            # Create a list of tasks for making asynchronous rddequests
            tasks = [fetch_data(url,id, headers, session, dist,pattern) for id in range(1,3000)]

            #asynchronously
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())


