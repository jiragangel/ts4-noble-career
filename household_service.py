import services # type: ignore
from sims.sim_info_types import Gender # type: ignore
import random
from datetime import datetime

# 2. Name Lists
female_names = [
    "Ava","Olivia","Emma","Charlotte","Amelia","Sophia","Isabella","Mia","Evelyn","Harper",
    "Luna","Ella","Abigail","Emily","Elizabeth","Sofia","Avery","Scarlett","Grace","Chloe",
    "Victoria","Riley","Aria","Lily","Aubrey","Zoey","Penelope","Lillian","Addison","Layla",
    "Natalie","Camila","Hannah","Brooklyn","Zoe","Nora","Leah","Savannah","Audrey","Claire",
    "Eleanor","Skylar","Ellie","Samantha","Stella","Paisley","Violet","Mila","Allison","Alexa",
    "Lucy","Madelyn","Bella","Julia","Piper","Hailey","Kinsley","Sadie","Autumn","Naomi",
    "Caroline","Genesis","Kennedy","Serenity","Maya","Sarah","Eva","Ariana","Quinn","Lydia",
    "Jade","Brianna","Adeline","Vivian","Willow","Reagan","Faith","Rose","Melanie","Eliza",
    "Isabelle","Valerie","Margaret","Ivy","Trinity","Emilia","Delilah","Josie","Ruby","Kaylee",
    "Taylor","Lyla","Katherine","Alexis","London","Payton","Brielle","Clara","Hadley","Eden",
    "Madeline","Alyssa","Nova","Isla","Nevaeh","Sloane","Elena","Kehlani","Blair","Mackenzie",
    "Juliana","Finley","Ariel","Phoebe","Daisy","Joanna","Tessa","Genevieve","Molly","Summer",
    "Nicole","Cecilia","Brooke","Lila","Ruth","Hope","Fiona","Annabelle","Jordyn","Noelle",
    "Rebecca","Bailey","Marley","Georgia","Alana","June","Kimberly","Veronica","Diana","Sabrina",
    "Angelina","Miranda","Rosalie","Helena","Annie","Paige","Shiloh","Teagan","Hallie","Rowan",
    "Zara","Emery","Aspen","Blake","Kaitlyn","Lola","Sienna","Margot","Willa","Peyton",
    "Lauren","Bethany","Delaney","Kara","Talia","Megan","Leslie","Cassidy","Danielle","Bryn",
    "Selena","Sage","Renee","Jenna","Ainsley","Lennon","Kelsey","Harley","Tatum","Oakley"
]


male_names = [
    "Liam","Noah","Oliver","Elijah","James","William","Benjamin","Lucas","Henry","Theodore",
    "Jack","Levi","Alexander","Jackson","Mateo","Daniel","Michael","Mason","Sebastian","Ethan",
    "Logan","Owen","Samuel","Jacob","Asher","Aiden","John","Joseph","Wyatt","David",
    "Leo","Luke","Julian","Hudson","Grayson","Matthew","Ezra","Gabriel","Carter","Isaac",
    "Jayden","Luca","Anthony","Dylan","Lincoln","Thomas","Maverick","Elias","Josiah","Charles",
    "Caleb","Christopher","Ezekiel","Miles","Jaxon","Isaiah","Andrew","Joshua","Nathan","Nolan",
    "Adrian","Cameron","Eli","Aaron","Ryan","Angel","Cooper","Waylon","Easton","Kai",
    "Christian","Landon","Colton","Roman","Axel","Brooks","Jonathan","Robert","Jameson","Ian",
    "Everett","Greyson","Wesley","Hunter","Leonardo","Bennett","Silas","Micah","Parker","Weston",
    "Brayden","Jordan","Jeremiah","Gavin","Nicholas","Austin","Adam","Evan","Dominic","Jose",
    "Jace","Julio","Kevin","Brandon","Tyler","Zachary","Eric","Connor","Diego","Calvin",
    "Antonio","Justin","Steven","Ayden","Jesse","Miguel","Vincent","Patrick","Kyle","Colin",
    "Marcus","Damian","Joel","Max","Jeremy","George","Emmanuel","Trevor","Riley","Victor",
    "Bryce","Luis","Jared","Grant","Oscar","Malachi","Xavier","Timothy","Emilio","Paul",
    "Brady","Colt","Alan","Brody","Derek","Jude","Peter","Tucker","Avery","Blake",
    "Rafael","Brent","Scott","Spencer","Mitchell","Dean","Hayden","Shawn","Travis","Marshall",
    "Jasper","Rowan","Sawyer","Finn","Holden","Reed","Cole","Ellis","Beckett","Arthur",
    "Simon","Theo","Sterling","Zane","Preston","Harrison","Clayton","Warren","Graham","Bryan",
    "Corey","Dustin","Franklin","Garrett","Howard","Russell","Troy","Victor-James","Wallace","Wade"
]


surnames = [
"Montgomery","Harrington","Wellington","Ashford","Kensington","Sinclair","Fairfax","Whitmore","Langston","Beaumont",
"Blackwood","Rutherford","Kingsley","Pembroke","Westminster","Hollingsworth","Huntington","Chatsworth","Cavendish","Winthrop",
"Rockefeller","Livingston","Hawthorne","Sterling","Huxley","Ellington","Prescott","Holloway","Barrington","Worthington",
"Remington","Thornbridge","Ainsworth","Carnegie","Vanderbilt","Lockwood","Fitzroy","Haversham","Lancaster","Bellingham",
"Middleton","Northington","Templeton","Loxley","Briarwood","Redgrave","Snowdon","Arlington","Whitfield","Kingsbridge",
"Goldsworth","Pembury","Dunham","Marbury","Clayborne","Hendrixon","Everton","Bellamy","Grantham","Marlowe",
"Westbrook","Summerton","Stratford","Rosewood","Kingsmoor","Brighton","Tennyson","Huntingford","Bridgerton","Kingsford",
"Stonebridge","Winterton","Mayfair","Belmont","Ashcroft","Thornton","Chadwick","Delafield","Gloucester","Rivington",
"Kingswell","Montague","Sherwood","Hampstead","Broadmoor","Fleetwood","Foxworth","Pemberton","Willoughby","Courtland",
"Brookfield","Cromwell","Kingsport","Albright","Hadleigh","Brunswick","Whitestone","Farringdon","Eastwood","Stirling",
"Kingsbury","Holliday","Blakemore","Manningham","Norwood","Greenwich","Parkhurst","Wentworth","Waverly","Bancroft",
"Radcliffe","Hargrave","Kingshall","Tolliver","Westfield","Beckwith","Harriman","Longfellow","Wakefield","Fairbourne",
"Kingsmont","Hampton","Strathmore","Golding","Ravenswood","Northfield","Bridgewater","Southwick","Kingsworth","Painswick",
"Aberdeen","Cedarwood","Kingsland","Kingsport","Brightwell","Merrifield","Hartwell","Windsor","Cranbrook","Hathersage",
"Kingsmere","Oakwood","Rothwell","Chilton","Whitcombe","Barclay","Hillsborough","Kingsfall","Northmoor","Fairmont",
"Windermere","Snowfield","Lockhart","Ashbourne","Winterbourne","Clearwater","Highfield","Kingsridge","Glenwood","Kingsvale",
"Foxbury","Harrowgate","Stonehurst","Westvale","Kingshaven","Brightmere","Rosemont","Silverstone","Kingscrest","Hedington",
"Amberton","Northvale","Bramwell","Kingswatch","Oakridge","Haverford","Brookstone","Kingslake","Whitlock","Kingscourt"
]

def update_all_household_funds(amount: int, output_func):
    household_manager = services.household_manager()
    count = 0
    for household in household_manager.get_all():
        try:
            household.funds.add(amount, 1)
            count += 1
        except Exception as e:
            output_func(f"Error updating household: {e}")
    output_func(f"Updated {count} households.")

def get_spouse_info_by_id(sim_id):
    """
    Core function to safely retrieve a spouse's SimInfo object.
    """
    sim_info_manager = services.sim_info_manager()
    sim_info = sim_info_manager.get(sim_id)
    
    if sim_info is None:
        return None

    # Use the built-in spouse_sim_id property
    # This returns 0 if they are not married
    spouse_id = sim_info.spouse_sim_id
    
    if spouse_id:
        return sim_info_manager.get(spouse_id)
    
    return None

def randomize_townie_marriage_names(output):
    try:
        active_household_id = services.active_household_id()
        
        processed_sim_ids = set()
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if not surnames:
                break

            if sim_info.sim_id in processed_sim_ids or sim_info.household_id == active_household_id:
                continue

            if sim_info.gender != Gender.FEMALE: 
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    new_surname = random.choice(surnames)
                    surnames.remove(new_surname)
                    
                    new_female_fn = random.choice(female_names)
                    new_male_fn = random.choice(male_names)

                    old_names = f"{sim_info.first_name} {sim_info.last_name} & {spouse_info.first_name} {spouse_info.last_name}"
                    
                    sim_info.first_name = new_female_fn
                    sim_info.last_name = new_surname
                    spouse_info.first_name = new_male_fn
                    spouse_info.last_name = new_surname
                    
                    processed_sim_ids.add(sim_info.sim_id)
                    processed_sim_ids.add(spouse_info.sim_id)
                    
                    count += 1
                    log_msg = f"SUCCESS: {old_names} -> {new_female_fn} & {new_male_fn} {new_surname}"
                    output(log_msg)

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1

        final_msg = f"Completed. Updated {count} couples. Errors: {error_count}"
        output(final_msg)
        return True

    except Exception as e:
        output(f"Crash: {str(e)}")
        return False

def randomize_townie_unmarried(output):
    try:
        active_household_id = services.active_household_id()
        
        count = 0
        error_count = 0

        all_sims = list(services.sim_info_manager().get_all())

        for sim_info in all_sims:
            if sim_info is None or not hasattr(sim_info, 'sim_id'):
                continue

            if not surnames:
                break

            if sim_info.household_id == active_household_id:
                continue

            try:
                spouse_info = get_spouse_info_by_id(sim_info.sim_id)
                
                if spouse_info:
                    output(f'{sim_info.first_name} {sim_info.last_name} has spouse')
                    continue

                new_surname = random.choice(surnames)
                surnames.remove(new_surname)
                
                new_firstname = ''
                
                if sim_info.gender != Gender.FEMALE:
                    new_firstname = random.choice(female_names)
                else:
                    new_firstname = random.choice(male_names)
                    
                old_names = f"{sim_info.first_name} {sim_info.last_name}"
                
                sim_info.first_name = new_firstname
                sim_info.last_name = new_surname
                
                count += 1
                log_msg = f"SUCCESS: {old_names} -> {new_firstname} {new_surname}"
                output(log_msg)

            except Exception as e:
                output(f"ERR Sim {sim_info.sim_id}: {str(e)}")
                error_count += 1

        final_msg = f"Completed. Updated {count} couples. Errors: {error_count}"
        output(final_msg)
        return True

    except Exception as e:
        output(f"Crash: {str(e)}")
        return False
    