"""
build_breeds_json.py
====================
Compiles comprehensive, accurate breed information for all 120 dog breeds
in model/class_names.txt and saves it to database/breeds_data.json.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'class_names.txt')
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, 'database', 'breeds_data.json')

with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
    breed_ids = [line.strip() for line in f if line.strip()]

# Reference encyclopedia dictionary mapping breed IDs to standard characteristics
BREED_DETAILS = {
    'affenpinscher': {
        'name': 'Affenpinscher',
        'size': 'Small',
        'temperament': 'Curious, Playful, Adventurous, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Germany',
        'description': 'Known as the "Monkey Terrier", this small toy breed has a distinctive bearded face, courageous demeanor, and lively personality.'
    },
    'afghan_hound': {
        'name': 'Afghan Hound',
        'size': 'Large',
        'temperament': 'Aloof, Dignified, Independent, Sweet',
        'lifespan': '12 - 14 years',
        'origin': 'Afghanistan',
        'description': 'An ancient sighthound known for its dramatic flowing silky coat, aristocratic bearing, and incredible hunting speed.'
    },
    'african_hunting_dog': {
        'name': 'African Hunting Dog',
        'size': 'Large',
        'temperament': 'Social, Highly Intelligent, Cooperative, Energetic',
        'lifespan': '10 - 12 years',
        'origin': 'Sub-Saharan Africa',
        'description': 'Also known as the African Painted Dog, recognized for its uniquely patterned calico-colored coat, large rounded ears, and tight pack structure.'
    },
    'airedale': {
        'name': 'Airedale Terrier',
        'size': 'Large',
        'temperament': 'Friendly, Clever, Courageous, Alert',
        'lifespan': '11 - 14 years',
        'origin': 'United Kingdom',
        'description': 'The largest of all terrier breeds, known as the "King of Terriers", versatile as a hunter, family protector, and sporting partner.'
    },
    'american_staffordshire_terrier': {
        'name': 'American Staffordshire Terrier',
        'size': 'Medium',
        'temperament': 'Confident, Good-natured, Loyal, Courageous',
        'lifespan': '12 - 16 years',
        'origin': 'United States',
        'description': 'A muscular, agile breed with remarkable loyalty and affection toward family when properly socialized and trained.'
    },
    'appenzeller': {
        'name': 'Appenzeller Sennenhund',
        'size': 'Medium',
        'temperament': 'Energetic, Reliable, Intelligent, Lively',
        'lifespan': '12 - 15 years',
        'origin': 'Switzerland',
        'description': 'A traditional Swiss mountain dog bred for herding cattle, featuring a distinctive tricolor coat and ringing bark.'
    },
    'australian_terrier': {
        'name': 'Australian Terrier',
        'size': 'Small',
        'temperament': 'Spirited, Alert, Courageous, Loyal',
        'lifespan': '11 - 15 years',
        'origin': 'Australia',
        'description': 'A sturdy, rough-coated little terrier bred to hunt rodents and small reptiles in the harsh Australian outback.'
    },
    'basenji': {
        'name': 'Basenji',
        'size': 'Small',
        'temperament': 'Independent, Quiet, Intelligent, Curious',
        'lifespan': '13 - 14 years',
        'origin': 'Democratic Republic of the Congo',
        'description': 'The famous "barkless dog" of central Africa, known for producing a unique yodel-like sound and grooming itself like a cat.'
    },
    'basset': {
        'name': 'Basset Hound',
        'size': 'Medium',
        'temperament': 'Patient, Low-key, Charming, Tenacious',
        'lifespan': '12 - 13 years',
        'origin': 'France',
        'description': 'An easygoing scent hound with short legs, long velvety ears, and a powerful sense of smell second only to the Bloodhound.'
    },
    'beagle': {
        'name': 'Beagle',
        'size': 'Small',
        'temperament': 'Merry, Friendly, Curious, Determined',
        'lifespan': '10 - 15 years',
        'origin': 'United Kingdom',
        'description': 'A beloved compact hound with an exceptional sense of smell, musical howl, and gentle, family-loving disposition.'
    },
    'bedlington_terrier': {
        'name': 'Bedlington Terrier',
        'size': 'Medium',
        'temperament': 'Loyal, Affectionate, Intelligent, Spirited',
        'lifespan': '11 - 16 years',
        'origin': 'United Kingdom',
        'description': 'Known for its distinctive lamb-like appearance with a woolly, pear-shaped head, yet possessing true terrier tenacity.'
    },
    'bernese_mountain_dog': {
        'name': 'Bernese Mountain Dog',
        'size': 'Large',
        'temperament': 'Good-natured, Calm, Strong, Devoted',
        'lifespan': '7 - 10 years',
        'origin': 'Switzerland',
        'description': 'A gentle giant bred for draft work in the Swiss Alps, adorned with a lustrous tricolor coat and a warm, affectionate heart.'
    },
    'black-and-tan_coonhound': {
        'name': 'Black and Tan Coonhound',
        'size': 'Large',
        'temperament': 'Even-tempered, Mellow, Easygoing, Tenacious',
        'lifespan': '10 - 12 years',
        'origin': 'United States',
        'description': 'An all-American trailing hound bred to track raccoons and deer with deep ringing baying and remarkable endurance.'
    },
    'blenheim_spaniel': {
        'name': 'Blenheim Spaniel',
        'size': 'Small',
        'temperament': 'Affectionate, Gentle, Graceful, Playful',
        'lifespan': '12 - 14 years',
        'origin': 'United Kingdom',
        'description': 'The rich red-and-white variety of the English Toy Spaniel, historically cherished as royal lap companions.'
    },
    'bloodhound': {
        'name': 'Bloodhound',
        'size': 'Large',
        'temperament': 'Gentle, Affectionate, Noble, Stubborn',
        'lifespan': '10 - 12 years',
        'origin': 'Belgium / France',
        'description': 'World-famous for having the most powerful scenting ability among all canines, with deep soulful wrinkles and droopy ears.'
    },
    'bluetick': {
        'name': 'Bluetick Coonhound',
        'size': 'Large',
        'temperament': 'Friendly, Intelligent, Devoted, Active',
        'lifespan': '11 - 12 years',
        'origin': 'United States',
        'description': 'An athletic hunting hound recognized by its mottled dark-blue coat, keen scenting prowess, and melodious tracking voice.'
    },
    'border_collie': {
        'name': 'Border Collie',
        'size': 'Medium',
        'temperament': 'Remarkably Intelligent, Energetic, Eager, Alert',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'Widely regarded as the most intelligent dog breed in the world, famous for its intense herding gaze and unmatched agility.'
    },
    'border_terrier': {
        'name': 'Border Terrier',
        'size': 'Small',
        'temperament': 'Affectionate, Plucky, Inquisitive, Alert',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'A tough, working terrier with an otter-shaped head, wiry weatherproof coat, and friendly, good-natured demeanor.'
    },
    'borzoi': {
        'name': 'Borzoi',
        'size': 'Large',
        'temperament': 'Quiet, Independent, Gentle, Aristocratic',
        'lifespan': '9 - 14 years',
        'origin': 'Russia',
        'description': 'Formerly known as the Russian Wolfhound, celebrated for its stately elegance, silky coat, and blistering speed across open steppes.'
    },
    'boston_bull': {
        'name': 'Boston Terrier',
        'size': 'Small',
        'temperament': 'Friendly, Bright, Amusing, Lively',
        'lifespan': '11 - 13 years',
        'origin': 'United States',
        'description': 'Nicknamed "The American Gentleman" because of its tuxedo-like coat markings, compact build, and polite household manners.'
    },
    'bouvier_des_flandres': {
        'name': 'Bouvier des Flandres',
        'size': 'Large',
        'temperament': 'Gentle, Loyal, Protective, Intelligent',
        'lifespan': '10 - 12 years',
        'origin': 'Belgium',
        'description': 'A powerful, rough-coated farm dog originally used for driving cattle, pulling carts, and guarding properties.'
    },
    'boxer': {
        'name': 'Boxer',
        'size': 'Large',
        'temperament': 'Playful, Energetic, Loyal, Fearless',
        'lifespan': '10 - 12 years',
        'origin': 'Germany',
        'description': 'An athletic, square-jawed working dog known for its youthful exuberance, love of children, and watchful protective nature.'
    },
    'brabancon_griffon': {
        'name': 'Brabancon Griffon',
        'size': 'Small',
        'temperament': 'Self-important, Inquisitive, Alert, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Belgium',
        'description': 'The smooth-coated variety of the Brussels Griffon, sporting an expressive, almost human-like face and lively personality.'
    },
    'briard': {
        'name': 'Briard',
        'size': 'Large',
        'temperament': 'Confident, Smart, Faithful, Brave',
        'lifespan': '12 - 12 years',
        'origin': 'France',
        'description': 'An ancient French herding and guard breed with a long wavy coat, peekaboo bangs, and strong devotion to its human flock.'
    },
    'brittany_spaniel': {
        'name': 'Brittany Spaniel',
        'size': 'Medium',
        'temperament': 'Bright, Fun-loving, Eager to Please, Quick',
        'lifespan': '12 - 14 years',
        'origin': 'France',
        'description': 'A versatile pointing gun dog with boundless energy, compact build, and keen sporting instincts in the field.'
    },
    'bull_mastiff': {
        'name': 'Bullmastiff',
        'size': 'Giant',
        'temperament': 'Affectionate, Loyal, Reserved, Courageous',
        'lifespan': '7 - 9 years',
        'origin': 'United Kingdom',
        'description': 'Bred by gamekeepers to track and hold poachers, this massive yet gentle guardian is quiet and remarkably docile at home.'
    },
    'cairn': {
        'name': 'Cairn Terrier',
        'size': 'Small',
        'temperament': 'Alert, Cheerful, Curious, Fearless',
        'lifespan': '13 - 15 years',
        'origin': 'Scotland',
        'description': 'Famous as "Toto" in The Wizard of Oz, a rugged Scottish terrier bred to dig into rocky cairns for vermin.'
    },
    'cardigan': {
        'name': 'Cardigan Welsh Corgi',
        'size': 'Small',
        'temperament': 'Affectionate, Loyal, Smart, Adaptable',
        'lifespan': '12 - 15 years',
        'origin': 'Wales',
        'description': 'The older of the two Corgi breeds, recognized by its long fox-like tail, low-slung frame, and vigilant cattle-herding instincts.'
    },
    'chesapeake_bay_retriever': {
        'name': 'Chesapeake Bay Retriever',
        'size': 'Large',
        'temperament': 'Affectionate, Bright, Courageous, Hardworking',
        'lifespan': '10 - 13 years',
        'origin': 'United States',
        'description': 'A rugged water dog with a waterproof oily wavy coat, built to brave icy waters and retrieve waterfowl along the mid-Atlantic coast.'
    },
    'chihuahua': {
        'name': 'Chihuahua',
        'size': 'Small',
        'temperament': 'Charming, Graceful, Sassy, Loyal',
        'lifespan': '14 - 16 years',
        'origin': 'Mexico',
        'description': 'The world\'s smallest purebred dog with an apple-dome skull, enormous personality, and fierce devotion to its chosen person.'
    },
    'chow': {
        'name': 'Chow Chow',
        'size': 'Medium',
        'temperament': 'Dignified, Bright, Serious, Aloof',
        'lifespan': '8 - 12 years',
        'origin': 'China',
        'description': 'An ancient lion-like breed famed for its blue-black tongue, deep-set eyes, thick ruff, and cat-like independence.'
    },
    'clumber': {
        'name': 'Clumber Spaniel',
        'size': 'Large',
        'temperament': 'Gentle, Loyal, Affectionate, Dignified',
        'lifespan': '10 - 12 years',
        'origin': 'United Kingdom',
        'description': 'The heaviest of the flushing spaniels, combining massive bone structure with a calm, sweet-tempered disposition.'
    },
    'cocker_spaniel': {
        'name': 'Cocker Spaniel',
        'size': 'Small',
        'temperament': 'Gentle, Smart, Happy, Trustworthy',
        'lifespan': '10 - 14 years',
        'origin': 'United States / United Kingdom',
        'description': 'A cheerful companion with big, expressive dark eyes, long silky feathered ears, and an ever-wagging tail.'
    },
    'collie': {
        'name': 'Rough Collie',
        'size': 'Large',
        'temperament': 'Graceful, Devoted, Proud, Intelligent',
        'lifespan': '12 - 14 years',
        'origin': 'Scotland',
        'description': 'Celebrated through the famous character "Lassie", noted for its long lush coat, wedge-shaped head, and intuitive bond with children.'
    },
    'curly-coated_retriever': {
        'name': 'Curly-Coated Retriever',
        'size': 'Large',
        'temperament': 'Confident, Clever, Proud, Independent',
        'lifespan': '10 - 12 years',
        'origin': 'United Kingdom',
        'description': 'One of the oldest retriever breeds, easily distinguished by its tight, water-repellent mass of crisp small curls.'
    },
    'dandie_dinmont': {
        'name': 'Dandie Dinmont Terrier',
        'size': 'Small',
        'temperament': 'Independent, Smart, Affectionate, Plucky',
        'lifespan': '12 - 15 years',
        'origin': 'Scotland',
        'description': 'A unique terrier with a distinctive powder-puff topknot of hair, long curved body, and calm, digniﬁed personality.'
    },
    'dhole': {
        'name': 'Dhole',
        'size': 'Medium',
        'temperament': 'Wild, Highly Social, Cautious, Alert',
        'lifespan': '10 - 13 years',
        'origin': 'Central & South Asia',
        'description': 'Also known as the Asiatic Wild Dog, a native canid living in cooperative social packs across the Asian forests.'
    },
    'dingo': {
        'name': 'Dingo',
        'size': 'Medium',
        'temperament': 'Independent, Cautious, Agile, Intelligent',
        'lifespan': '12 - 15 years',
        'origin': 'Australia',
        'description': 'Australia\'s native wild canid, possessing remarkable flexible joints, erect ears, and exceptional survival instincts in the outback.'
    },
    'doberman': {
        'name': 'Doberman Pinscher',
        'size': 'Large',
        'temperament': 'Loyal, Fearless, Alert, Highly Intelligent',
        'lifespan': '10 - 12 years',
        'origin': 'Germany',
        'description': 'A sleek, muscular protector combining aristocratic elegance with world-class guardian instincts and deep family loyalty.'
    },
    'english_foxhound': {
        'name': 'English Foxhound',
        'size': 'Large',
        'temperament': 'Friendly, Active, Gentle, Pack-oriented',
        'lifespan': '10 - 13 years',
        'origin': 'United Kingdom',
        'description': 'A stout, muscular scent hound bred for pack endurance, known for its stamina and harmonious pack-hunting bay.'
    },
    'english_setter': {
        'name': 'English Setter',
        'size': 'Large',
        'temperament': 'Gentle, Affectionate, Friendly, Mellow',
        'lifespan': '12 - 12 years',
        'origin': 'United Kingdom',
        'description': 'Known as the "Gentleman of the Dog World", sporting a gorgeous speckled "belton" coat and mild, loving temperament.'
    },
    'english_springer': {
        'name': 'English Springer Spaniel',
        'size': 'Medium',
        'temperament': 'Friendly, Playful, Eager to Please, Cheerful',
        'lifespan': '12 - 14 years',
        'origin': 'United Kingdom',
        'description': 'A lively sporting dog built to flush and spring game, prized by families for its enthusiastic companionship and trainability.'
    },
    'entlebucher': {
        'name': 'Entlebucher Mountain Dog',
        'size': 'Medium',
        'temperament': 'Enthusiastic, Loyal, Agile, Clever',
        'lifespan': '11 - 13 years',
        'origin': 'Switzerland',
        'description': 'The smallest of the Swiss Mountain Dogs, famous for its quick speed, cattle-droving stamina, and striking tricolor coat.'
    },
    'eskimo_dog': {
        'name': 'American Eskimo Dog',
        'size': 'Small',
        'temperament': 'Playful, Bright, Perky, Alert',
        'lifespan': '13 - 15 years',
        'origin': 'Germany / United States',
        'description': 'A stunning Nordic spitz with a cloud-white double coat, keen smiling expression, and high aptitude for tricks and agility.'
    },
    'flat-coated_retriever': {
        'name': 'Flat-Coated Retriever',
        'size': 'Large',
        'temperament': 'Optimistic, Outgoing, Good-humored, Devoted',
        'lifespan': '8 - 10 years',
        'origin': 'United Kingdom',
        'description': 'Nicknamed the "Peter Pan of retrievers" because of its lifelong puppy-like spirit, glossy black coat, and wagging tail.'
    },
    'french_bulldog': {
        'name': 'French Bulldog',
        'size': 'Small',
        'temperament': 'Adaptable, Playful, Smart, Affectionate',
        'lifespan': '10 - 12 years',
        'origin': 'France',
        'description': 'One of the most popular companion dogs worldwide, recognized by its trademark bat ears, compact frame, and quiet charm.'
    },
    'german_shepherd': {
        'name': 'German Shepherd',
        'size': 'Large',
        'temperament': 'Confident, Courageous, Smart, Loyal',
        'lifespan': '10 - 13 years',
        'origin': 'Germany',
        'description': 'A capable, noble working dog widely serving in police, service, and search-and-rescue roles with unwavering devotion.'
    },
    'german_short-haired_pointer': {
        'name': 'German Shorthaired Pointer',
        'size': 'Large',
        'temperament': 'Friendly, Intelligent, Willing to Please, Enthusiastic',
        'lifespan': '10 - 12 years',
        'origin': 'Germany',
        'description': 'An all-around versatile hunting partner capable of pointing, retrieving, and tracking across land and water.'
    },
    'giant_schnauzer': {
        'name': 'Giant Schnauzer',
        'size': 'Giant',
        'temperament': 'Loyal, Alert, Powerful, Intelligent',
        'lifespan': '12 - 15 years',
        'origin': 'Germany',
        'description': 'A commanding, bearded working breed combining towering strength with sharp intelligence and vigilant protective instincts.'
    },
    'golden_retriever': {
        'name': 'Golden Retriever',
        'size': 'Large',
        'temperament': 'Intelligent, Friendly, Devoted, Reliable',
        'lifespan': '10 - 12 years',
        'origin': 'Scotland',
        'description': 'A world-famous family companion and guide dog with a radiant golden coat, warm expression, and eagerness to please.'
    },
    'gordon_setter': {
        'name': 'Gordon Setter',
        'size': 'Large',
        'temperament': 'Confident, Affectionate, Bold, Loyal',
        'lifespan': '12 - 13 years',
        'origin': 'Scotland',
        'description': 'The largest and heaviest of the setter family, featuring a rich black-and-tan coat and steadfast devotion to its family.'
    },
    'great_dane': {
        'name': 'Great Dane',
        'size': 'Giant',
        'temperament': 'Friendly, Patient, Dependable, Gentle',
        'lifespan': '7 - 10 years',
        'origin': 'Germany',
        'description': 'The "Apollo of Dogs", towering in size yet famously gentle, patient with children, and peaceful in the home.'
    },
    'great_pyrenees': {
        'name': 'Great Pyrenees',
        'size': 'Giant',
        'temperament': 'Patient, Calm, Gentle, Fearless',
        'lifespan': '10 - 12 years',
        'origin': 'France / Spain',
        'description': 'A majestic white guardian bred to protect sheep flocks from wolves in the snowy Pyrenees Mountains.'
    },
    'greater_swiss_mountain_dog': {
        'name': 'Greater Swiss Mountain Dog',
        'size': 'Giant',
        'temperament': 'Faithful, Alert, Good-natured, Calm',
        'lifespan': '8 - 11 years',
        'origin': 'Switzerland',
        'description': 'A heavy-boned, muscular draft dog renowned for pulling heavy milk carts across the Swiss countryside.'
    },
    'groenendael': {
        'name': 'Belgian Sheepdog (Groenendael)',
        'size': 'Large',
        'temperament': 'Intelligent, Active, Sensitive, Watchful',
        'lifespan': '12 - 14 years',
        'origin': 'Belgium',
        'description': 'A striking black-coated herding dog celebrated for its versatile intelligence, graceful agility, and deep loyalty.'
    },
    'ibizan_hound': {
        'name': 'Ibizan Hound',
        'size': 'Large',
        'temperament': 'Even-tempered, Playful, Polite, Fast',
        'lifespan': '11 - 14 years',
        'origin': 'Spain',
        'description': 'An ancient Mediterranean sighthound that leaps like a gazelle, recognized by its amber eyes and tall erect ears.'
    },
    'irish_setter': {
        'name': 'Irish Setter',
        'size': 'Large',
        'temperament': 'Outgoing, Sweet-tempered, Active, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Ireland',
        'description': 'Instantly recognizable by its glamorous mahogany-red coat, joyful rollicking spirit, and boundless athletic energy.'
    },
    'irish_terrier': {
        'name': 'Irish Terrier',
        'size': 'Medium',
        'temperament': 'Bold, Dashing, Courageous, Tenderhearted',
        'lifespan': '13 - 15 years',
        'origin': 'Ireland',
        'description': 'Known as the "Daredevil of the Emerald Isle", with a fiery red wiry coat, fearless courage, and loving family nature.'
    },
    'irish_water_spaniel': {
        'name': 'Irish Water Spaniel',
        'size': 'Large',
        'temperament': 'Playful, Brave, Intelligent, Inquisitive',
        'lifespan': '12 - 13 years',
        'origin': 'Ireland',
        'description': 'The clown of the spaniel family, known for its dense liver curls, distinctive rat-like tail, and topknot of curls.'
    },
    'irish_wolfhound': {
        'name': 'Irish Wolfhound',
        'size': 'Giant',
        'temperament': 'Courageous, Dignified, Calm, Gentle',
        'lifespan': '6 - 8 years',
        'origin': 'Ireland',
        'description': 'The tallest of all dog breeds, historic hunters of wolves whose serene gentleness earned the motto "gentle when stroked, fierce when provoked".'
    },
    'italian_greyhound': {
        'name': 'Italian Greyhound',
        'size': 'Small',
        'temperament': 'Sensitive, Alert, Playful, Affectionate',
        'lifespan': '14 - 15 years',
        'origin': 'Italy',
        'description': 'A delicate miniature sighthound adored since Renaissance nobility, combining lightning sprint speed with supreme cuddle affection.'
    },
    'japanese_spaniel': {
        'name': 'Japanese Chin',
        'size': 'Small',
        'temperament': 'Charming, Noble, Loving, Quiet',
        'lifespan': '10 - 12 years',
        'origin': 'Japan',
        'description': 'An aristocratic lap companion of Japanese royalty, known for its cat-like agility, plumed tail, and expressive wide eyes.'
    },
    'keeshond': {
        'name': 'Keeshond',
        'size': 'Medium',
        'temperament': 'Friendly, Lively, Outgoing, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Netherlands',
        'description': 'The Dutch barge dog, famed for its plush silver-and-black coat, curled tail, and dark "spectacle" markings around the eyes.'
    },
    'kelpie': {
        'name': 'Australian Kelpie',
        'size': 'Medium',
        'temperament': 'Loyal, Tireless, Eager, Highly Intelligent',
        'lifespan': '12 - 15 years',
        'origin': 'Australia',
        'description': 'A legendary Australian herding dog possessing inexhaustible stamina, capable of managing large sheep mobs in blistering heat.'
    },
    'kerry_blue_terrier': {
        'name': 'Kerry Blue Terrier',
        'size': 'Medium',
        'temperament': 'Smart, Spirited, Loyal, People-oriented',
        'lifespan': '12 - 15 years',
        'origin': 'Ireland',
        'description': 'The national terrier of Ireland, recognized for its striking blue-gray wavy coat and versatile all-around farm utility.'
    },
    'komondor': {
        'name': 'Komondor',
        'size': 'Giant',
        'temperament': 'Loyal, Dignified, Brave, Independent',
        'lifespan': '10 - 12 years',
        'origin': 'Hungary',
        'description': 'The "mop dog" of Hungary, covered in dense heavy white cords that protect it from predators and extreme weather while guarding sheep.'
    },
    'kuvasz': {
        'name': 'Kuvasz',
        'size': 'Giant',
        'temperament': 'Protective, Loyal, Patient, Courageous',
        'lifespan': '10 - 12 years',
        'origin': 'Hungary',
        'description': 'An ancient royal Hungarian flock guardian with a dense white coat, commanding presence, and fierce loyalty to its family.'
    },
    'labrador_retriever': {
        'name': 'Labrador Retriever',
        'size': 'Large',
        'temperament': 'Friendly, Active, Outgoing, Gentle',
        'lifespan': '11 - 13 years',
        'origin': 'Canada / United Kingdom',
        'description': 'The most popular breed in the world for decades, famous for its water-repellent coat, otter tail, and warm, gentle disposition.'
    },
    'lakeland_terrier': {
        'name': 'Lakeland Terrier',
        'size': 'Small',
        'temperament': 'Bold, Friendly, Confident, Playful',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'Bred in the rugged English Lake District to protect sheepfolds from foxes, featuring a wiry jacket and fiery terrier courage.'
    },
    'leonberg': {
        'name': 'Leonberger',
        'size': 'Giant',
        'temperament': 'Gentle, Friendly, Intelligent, Playful',
        'lifespan': '7 - 9 years',
        'origin': 'Germany',
        'description': 'A lion-like gentle giant bred in Germany, famous for its black mask, luxurious double coat, and wonderful patience with children.'
    },
    'lhasa': {
        'name': 'Lhasa Apso',
        'size': 'Small',
        'temperament': 'Confident, Smart, Comical, Independent',
        'lifespan': '12 - 15 years',
        'origin': 'Tibet',
        'description': 'An ancient sentinel of Tibetan monasteries and palaces, boasting a floor-length parted coat and watchful protector instincts.'
    },
    'malamute': {
        'name': 'Alaskan Malamute',
        'size': 'Large',
        'temperament': 'Affectionate, Loyal, Playful, Devoted',
        'lifespan': '10 - 14 years',
        'origin': 'United States (Alaska)',
        'description': 'An arctic freighting sled dog possessing immense power, wolf-like facial markings, a plumed tail, and a warm pack spirit.'
    },
    'malinois': {
        'name': 'Belgian Malinois',
        'size': 'Large',
        'temperament': 'Confident, Hardworking, Highly Intelligent, Vigilant',
        'lifespan': '14 - 16 years',
        'origin': 'Belgium',
        'description': 'The premier working military and police dog in the world, prized for its laser focus, athletic speed, and tireless drive.'
    },
    'maltese_dog': {
        'name': 'Maltese',
        'size': 'Small',
        'temperament': 'Gentle, Playful, Charming, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Malta',
        'description': 'An ancient Mediterranean aristocrat with floor-sweeping silky white hair, dark soulful eyes, and a sweet, affectionate nature.'
    },
    'mexican_hairless': {
        'name': 'Xoloitzcuintli (Mexican Hairless)',
        'size': 'Medium',
        'temperament': 'Loyal, Alert, Calm, Intelligent',
        'lifespan': '13 - 18 years',
        'origin': 'Mexico',
        'description': 'An ancient sacred Aztec dog revered as a spiritual guide, characterized by smooth warm skin, bat-like ears, and serene loyalty.'
    },
    'miniature_pinscher': {
        'name': 'Miniature Pinscher',
        'size': 'Small',
        'temperament': 'Fearless, Proud, Energetic, Fun-loving',
        'lifespan': '12 - 16 years',
        'origin': 'Germany',
        'description': 'The "King of Toys", possessing a high-stepping hackney gait, sleek coat, and fearless self-confidence.'
    },
    'miniature_poodle': {
        'name': 'Miniature Poodle',
        'size': 'Small',
        'temperament': 'Exceptionally Intelligent, Active, Alert, Elegant',
        'lifespan': '14 - 18 years',
        'origin': 'France / Germany',
        'description': 'A versatile, athletic companion featuring a hypoallergenic curly coat and standing among the world\'s most trainable breeds.'
    },
    'miniature_schnauzer': {
        'name': 'Miniature Schnauzer',
        'size': 'Small',
        'temperament': 'Friendly, Intelligent, Alert, Obedient',
        'lifespan': '12 - 15 years',
        'origin': 'Germany',
        'description': 'Recognized by its bushy beard and expressive walrus eyebrows, a spunky and affectionate companion for any home.'
    },
    'newfoundland': {
        'name': 'Newfoundland',
        'size': 'Giant',
        'temperament': 'Sweet-tempered, Gentle, Patient, Devoted',
        'lifespan': '9 - 10 years',
        'origin': 'Canada',
        'description': 'Known as "nature\'s lifeguard" for saving drowning swimmers with its webbed paws, water-resistant coat, and sweet temperament.'
    },
    'norfolk_terrier': {
        'name': 'Norfolk Terrier',
        'size': 'Small',
        'temperament': 'Fearless, Affectionate, Spirited, Companionable',
        'lifespan': '12 - 16 years',
        'origin': 'United Kingdom',
        'description': 'One of the smallest working terriers, recognized by its drop ears, wiry coat, and big-dog courage in a pocket-sized package.'
    },
    'norwegian_elkhound': {
        'name': 'Norwegian Elkhound',
        'size': 'Medium',
        'temperament': 'Bold, Playful, Friendly, Dependable',
        'lifespan': '12 - 15 years',
        'origin': 'Norway',
        'description': 'An ancient Viking hound bred to hunt moose and bear in Scandinavia, sporting a thick silver-gray coat and tightly curled tail.'
    },
    'norwich_terrier': {
        'name': 'Norwich Terrier',
        'size': 'Small',
        'temperament': 'Affectionate, Plucky, Curious, Loyal',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'Distinguished from the Norfolk Terrier by its sharp prick ears, this lively rat-catcher makes a cheerful and sturdy companion.'
    },
    'old_english_sheepdog': {
        'name': 'Old English Sheepdog',
        'size': 'Large',
        'temperament': 'Adaptable, Gentle, Intelligent, Playful',
        'lifespan': '10 - 12 years',
        'origin': 'United Kingdom',
        'description': 'The famous shaggy "Bobtail" with a bear-like shuffle gait, sweet humorous personality, and heavy double coat.'
    },
    'otterhound': {
        'name': 'Otterhound',
        'size': 'Large',
        'temperament': 'Amiable, Boisterous, Even-tempered, Musical',
        'lifespan': '10 - 13 years',
        'origin': 'United Kingdom',
        'description': 'A rare British scent hound with webbed feet, rough waterproof coat, and a booming voice bred to hunt in water and mud.'
    },
    'papillon': {
        'name': 'Papillon',
        'size': 'Small',
        'temperament': 'Friendly, Alert, Happy, Energetic',
        'lifespan': '14 - 16 years',
        'origin': 'France',
        'description': 'Named after the French word for "butterfly" because of its large fringed wing-like ears, highly agile and remarkably smart.'
    },
    'pekinese': {
        'name': 'Pekingese',
        'size': 'Small',
        'temperament': 'Affectionate, Loyal, Regal, Opinionated',
        'lifespan': '12 - 14 years',
        'origin': 'China',
        'description': 'Bred for centuries by Chinese emperors, this "lion dog" walks with a dignified rolling gait and carries royal pride.'
    },
    'pembroke': {
        'name': 'Pembroke Welsh Corgi',
        'size': 'Small',
        'temperament': 'Affectionate, Smart, Alert, Outgoing',
        'lifespan': '12 - 13 years',
        'origin': 'Wales',
        'description': 'The beloved favorite breed of Queen Elizabeth II, featuring short legs, docked tail, big fox ears, and a boundless happy spirit.'
    },
    'pomeranian': {
        'name': 'Pomeranian',
        'size': 'Small',
        'temperament': 'Lively, Bold, Inquisitive, Playful',
        'lifespan': '12 - 16 years',
        'origin': 'Germany / Poland',
        'description': 'A pint-sized spitz with a magnificent puffed lion mane ruff, foxy face, and an extroverted vivacious personality.'
    },
    'pug': {
        'name': 'Pug',
        'size': 'Small',
        'temperament': 'Charming, Mischievous, Loving, Docile',
        'lifespan': '13 - 15 years',
        'origin': 'China',
        'description': 'Guided by the Latin motto "Multum in Parvo" (a lot in a little), beloved for its wrinkled brow, curled tail, and comic charm.'
    },
    'redbone': {
        'name': 'Redbone Coonhound',
        'size': 'Large',
        'temperament': 'Even-tempered, Friendly, Eager, Gentle',
        'lifespan': '12 - 15 years',
        'origin': 'United States',
        'description': 'A handsome Southern trailing hound clad in a gleaming solid-red coat, famous for its speed, sweet disposition, and mournful bay.'
    },
    'rhodesian_ridgeback': {
        'name': 'Rhodesian Ridgeback',
        'size': 'Large',
        'temperament': 'Dignified, Intelligent, Strong-willed, Loyal',
        'lifespan': '10 - 12 years',
        'origin': 'Zimbabwe / South Africa',
        'description': 'Originally bred to track lions in Africa, recognized by the backward-growing ridge of hair running down its spine.'
    },
    'rottweiler': {
        'name': 'Rottweiler',
        'size': 'Large',
        'temperament': 'Loyal, Loving, Confident Guardian, Calm',
        'lifespan': '9 - 10 years',
        'origin': 'Germany',
        'description': 'A robust working dog descended from Roman drover cattle dogs, known for its protective confidence and deep devotion to family.'
    },
    'saint_bernard': {
        'name': 'Saint Bernard',
        'size': 'Giant',
        'temperament': 'Inquisitive, Friendly, Calm, Gentle',
        'lifespan': '8 - 10 years',
        'origin': 'Switzerland',
        'description': 'The legendary alpine rescuer from the Great St. Bernard Hospice, famous for its giant heart, patient demeanor, and snow rescues.'
    },
    'saluki': {
        'name': 'Saluki',
        'size': 'Large',
        'temperament': 'Gentle, Aloof, Dignified, Independent',
        'lifespan': '12 - 14 years',
        'origin': 'Middle East',
        'description': 'An ancient royal sighthound of Egypt and Arabia, built for breathtaking desert hunting speed with feathered ears and tail.'
    },
    'samoyed': {
        'name': 'Samoyed',
        'size': 'Medium',
        'temperament': 'Friendly, Gentle, Adaptable, Playful',
        'lifespan': '12 - 14 years',
        'origin': 'Siberia (Russia)',
        'description': 'Known for the famous "Sammy smile" with upturned lips to prevent icicles, wrapped in a plush cloud of glistening white fur.'
    },
    'schipperke': {
        'name': 'Schipperke',
        'size': 'Small',
        'temperament': 'Confident, Alert, Curious, Tireless',
        'lifespan': '12 - 14 years',
        'origin': 'Belgium',
        'description': 'The "Little Captain" of Belgian canal barges, compact with a foxy head, thick black ruff, and curious, watchful nature.'
    },
    'scotch_terrier': {
        'name': 'Scottish Terrier',
        'size': 'Small',
        'temperament': 'Independent, Confident, Dignified, Spirited',
        'lifespan': '12 - 12 years',
        'origin': 'Scotland',
        'description': 'Nicknamed "The Diehard" for its rugged determination, sporting a distinctive beard, erect pointed ears, and dignified personality.'
    },
    'scottish_deerhound': {
        'name': 'Scottish Deerhound',
        'size': 'Giant',
        'temperament': 'Gentle, Dignified, Polite, Quiet',
        'lifespan': '8 - 11 years',
        'origin': 'Scotland',
        'description': 'The royal hound of Scotland bred to hunt red deer in the Highlands, combining towering height with a calm, sweet manner.'
    },
    'sealyham_terrier': {
        'name': 'Sealyham Terrier',
        'size': 'Small',
        'temperament': 'Affectionate, Calm, Comical, Determined',
        'lifespan': '12 - 14 years',
        'origin': 'Wales',
        'description': 'A sturdy white terrier developed in Wales, recognized by its fall of hair over the eyes, lavish beard, and humorous character.'
    },
    'shetland_sheepdog': {
        'name': 'Shetland Sheepdog (Sheltie)',
        'size': 'Small',
        'temperament': 'Playful, Energetic, Bright, Responsive',
        'lifespan': '12 - 14 years',
        'origin': 'Scotland (Shetland Islands)',
        'description': 'A miniature rough collie in looks, renowned for its agile herding skills, gentle obedience, and deep sensitivity to humans.'
    },
    'shih-tzu': {
        'name': 'Shih Tzu',
        'size': 'Small',
        'temperament': 'Affectionate, Playful, Outgoing, Loving',
        'lifespan': '10 - 18 years',
        'origin': 'Tibet / China',
        'description': 'The "Chrysanthemum Dog" bred as royal lap warmers for Chinese emperors, boasting a flowing double coat and warm heart.'
    },
    'siberian_husky': {
        'name': 'Siberian Husky',
        'size': 'Medium',
        'temperament': 'Loyal, Outgoing, Mischievous, Athletic',
        'lifespan': '12 - 14 years',
        'origin': 'Siberia (Russia)',
        'description': 'A graceful sled dog with piercing blue or multi-colored eyes, dense double coat, and musical talkative vocalizations.'
    },
    'silky_terrier': {
        'name': 'Silky Terrier',
        'size': 'Small',
        'temperament': 'Friendly, Quick, Alert, Inquisitive',
        'lifespan': '13 - 15 years',
        'origin': 'Australia',
        'description': 'A refined Australian toy terrier with a fine blue-and-tan silky coat that retains true spirited terrier prey drive.'
    },
    'soft-coated_wheaten_terrier': {
        'name': 'Soft Coated Wheaten Terrier',
        'size': 'Medium',
        'temperament': 'Happy, Deeply Devoted, Enthusiastic, Clever',
        'lifespan': '12 - 14 years',
        'origin': 'Ireland',
        'description': 'An all-purpose Irish farm dog clad in a soft, wavy coat the color of ripening wheat, known for greeting with enthusiastic joy.'
    },
    'staffordshire_bullterrier': {
        'name': 'Staffordshire Bull Terrier',
        'size': 'Medium',
        'temperament': 'Courageous, Intelligent, Loyal, Affectionate',
        'lifespan': '12 - 14 years',
        'origin': 'United Kingdom',
        'description': 'Nicknamed the "Nanny Dog" in Britain for its patient love of children, combining muscular athleticism with tender affection.'
    },
    'standard_poodle': {
        'name': 'Standard Poodle',
        'size': 'Large',
        'temperament': 'Active, Proud, Highly Intelligent, Loyal',
        'lifespan': '10 - 18 years',
        'origin': 'France / Germany',
        'description': 'Originally a water duck retriever, famous for its hypoallergenic non-shedding coat and top-tier problem-solving intelligence.'
    },
    'standard_schnauzer': {
        'name': 'Standard Schnauzer',
        'size': 'Medium',
        'temperament': 'Friendly, Intelligent, Devoted, Spirited',
        'lifespan': '13 - 16 years',
        'origin': 'Germany',
        'description': 'The original prototype of the schnauzer family, recognizable by its pepper-and-salt coat, bristly beard, and vigilant loyalty.'
    },
    'sussex_spaniel': {
        'name': 'Sussex Spaniel',
        'size': 'Medium',
        'temperament': 'Calm, Cheerful, Companionable, Devoted',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'A low-built, golden-liver hunting spaniel with a rolling gait and a cheerful habit of barking while scenting in the field.'
    },
    'tibetan_mastiff': {
        'name': 'Tibetan Mastiff',
        'size': 'Giant',
        'temperament': 'Independent, Reserved, Intelligent, Protective',
        'lifespan': '10 - 12 years',
        'origin': 'Tibet',
        'description': 'An awe-inspiring Himalayan guardian with a lion-like mane, ancient heritage, and solitary, independent protective instincts.'
    },
    'tibetan_terrier': {
        'name': 'Tibetan Terrier',
        'size': 'Medium',
        'temperament': 'Affectionate, Loyal, Sensitive, Clever',
        'lifespan': '15 - 16 years',
        'origin': 'Tibet',
        'description': 'The "Holy Dog of Tibet", possessing wide flat "snowshoe" feet, a profuse fall of hair, and ancient status as good-luck charms.'
    },
    'toy_poodle': {
        'name': 'Toy Poodle',
        'size': 'Small',
        'temperament': 'Agile, Intelligent, Self-confident, Alert',
        'lifespan': '10 - 18 years',
        'origin': 'France / Germany',
        'description': 'The smallest variety of Poodle, packing all the legendary intelligence and hypoallergenic coat of the standard into a tiny companion.'
    },
    'toy_terrier': {
        'name': 'English Toy Terrier',
        'size': 'Small',
        'temperament': 'Alert, Intelligent, Companionable, Courageous',
        'lifespan': '12 - 13 years',
        'origin': 'United Kingdom',
        'description': 'A sleek black-and-tan toy dog with candle-flame ears, graceful movement, and keen alert ratting instincts.'
    },
    'vizsla': {
        'name': 'Vizsla',
        'size': 'Medium',
        'temperament': 'Affectionate, Loyal, Energetic, Gentle',
        'lifespan': '12 - 14 years',
        'origin': 'Hungary',
        'description': 'The golden-rust pointer of Hungarian nobility, nicknamed the "Velcro dog" because of its desire to stay attached to its human.'
    },
    'walker_hound': {
        'name': 'Treeing Walker Coonhound',
        'size': 'Large',
        'temperament': 'Smart, Brave, Affectionate, Energetic',
        'lifespan': '12 - 13 years',
        'origin': 'United States',
        'description': 'Known as "the people\'s choice" coonhound, possessing lightning speed, treeing tenacity, and a clear ringing tracking bay.'
    },
    'weimaraner': {
        'name': 'Weimaraner',
        'size': 'Large',
        'temperament': 'Friendly, Fearless, Alert, Obedient',
        'lifespan': '10 - 13 years',
        'origin': 'Germany',
        'description': 'The "Gray Ghost" of the dog world, celebrated for its silvery sleek coat, amber eyes, and aristocratic hunting speed.'
    },
    'welsh_springer_spaniel': {
        'name': 'Welsh Springer Spaniel',
        'size': 'Medium',
        'temperament': 'Active, Loyal, Playful, Affectionate',
        'lifespan': '12 - 15 years',
        'origin': 'Wales',
        'description': 'An ancient gundog distinguished by its red-and-white coat, small vine-leaf ears, and loyal attachment to its family.'
    },
    'west_highland_white_terrier': {
        'name': 'West Highland White Terrier (Westie)',
        'size': 'Small',
        'temperament': 'Loyal, Happy, Entertaining, Hardy',
        'lifespan': '13 - 15 years',
        'origin': 'Scotland',
        'description': 'A charming Scottish terrier with a carrot-shaped tail, brilliant white double coat, and cheerful self-confidence.'
    },
    'whippet': {
        'name': 'Whippet',
        'size': 'Medium',
        'temperament': 'Affectionate, Playful, Quiet, Gentle',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'The "poor man\'s racehorse", reaching 35 mph speeds in open sprints yet functioning as a serene, peaceful couch lounger at home.'
    },
    'wire-haired_fox_terrier': {
        'name': 'Wire Fox Terrier',
        'size': 'Small',
        'temperament': 'Keen, Alert, Quick, Friendly',
        'lifespan': '12 - 15 years',
        'origin': 'United Kingdom',
        'description': 'A classic English terrier with a dense broken wiry jacket, V-shaped ears, and endless vivacious hunting energy.'
    },
    'yorkshire_terrier': {
        'name': 'Yorkshire Terrier (Yorkie)',
        'size': 'Small',
        'temperament': 'Affectionate, Sprightly, Tomboyish, Feisty',
        'lifespan': '11 - 15 years',
        'origin': 'United Kingdom',
        'description': 'One of the most glamorous toy breeds, sporting a floor-length blue-and-gold silky coat with the fearless spirit of a terrier.'
    }
}

# Generate complete data for all 120 breeds
dataset = []
for bid in breed_ids:
    if bid in BREED_DETAILS:
        info = BREED_DETAILS[bid]
    else:
        # Fallback formatting if any breed is unmapped
        formatted_name = ' '.join(w.capitalize() for w in bid.replace('_', ' ').replace('-', ' ').split())
        info = {
            'name': formatted_name,
            'size': 'Medium',
            'temperament': 'Loyal, Intelligent, Active',
            'lifespan': '10 - 14 years',
            'origin': 'Unknown',
            'description': f'A recognized purebred canine in the 120-class dataset with distinctive working and companion traits.'
        }

    dataset.append({
        'id': bid,
        'name': info['name'],
        'size': info['size'],
        'temperament': info['temperament'],
        'lifespan': info['lifespan'],
        'origin': info['origin'],
        'description': info['description'],
        'image': f'/static/images/breeds/{bid}.jpg'
    })

# Save to JSON
with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2)

print(f"[OK] Successfully built {len(dataset)} breed records in {OUTPUT_JSON_PATH}")
