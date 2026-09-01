# -*- coding: utf-8 -*-
"""
Content data for New Nest — free new-pet checklist printables.
Each species has 4 checklists: first-week, supplies, vet-visit, pet-proofing.
"""

SITE = {
    "name": "New Nest",
    "tagline": "Free checklists for the first days with a new pet.",
    "description": "Free printable checklists for new pet parents. First week plans, "
                   "supply lists, first vet visit prep, and home safety walk-throughs "
                   "for dogs, cats, rabbits, guinea pigs, and birds. No account, no email.",
    "url": "https://newnestpets.netlify.app",
    "color": "#c1694f",
    "color_dark": "#8f4835",
    "bg": "#faf5ef",
}

SPECIES = {
    "dog": {
        "label": "Dog",
        "emoji": "🐶",
        "blurb": "Your new best friend",
        "sort": 1,
    },
    "cat": {
        "label": "Cat",
        "emoji": "🐱",
        "blurb": "Your new independent shadow",
        "sort": 2,
    },
    "small-furry": {
        "label": "Rabbit & Guinea Pig",
        "emoji": "🐰",
        "blurb": "Small pets, big personalities",
        "sort": 3,
    },
    "bird": {
        "label": "Bird",
        "emoji": "🦜",
        "blurb": "Your new feathered flockmate",
        "sort": 4,
    },
}

CATEGORIES = {
    "first-week": {
        "title": "First Week Home Checklist",
        "short": "First week home",
        "desc": "Day-by-day settle-in tasks so the first week feels calm instead of chaotic.",
        "sort": 1,
    },
    "supplies": {
        "title": "New Pet Supply Shopping List",
        "short": "Supply shopping list",
        "desc": "Everything to have ready before, or right after, pickup day.",
        "sort": 2,
    },
    "vet-visit": {
        "title": "First Vet Visit Prep Sheet",
        "short": "First vet visit prep",
        "desc": "What to bring and what to ask at their first checkup.",
        "sort": 3,
    },
    "pet-proofing": {
        "title": "Home Safety Checklist",
        "short": "Home safety walk-through",
        "desc": "A room-by-room pass to make your home safer before they arrive.",
        "sort": 4,
    },
}

# ---------------------------------------------------------------------------
# Checklist items. Each is a list of (section_heading, [items]) tuples so the
# PDF and web worksheet can both group items under short headers.
# ---------------------------------------------------------------------------

CHECKLISTS = {
    ("dog", "first-week"): [
        ("Before they arrive", [
            "Set up a crate or designated sleep space in a quiet corner",
            "Pick up food and water bowls and place them in one steady spot",
            "Buy a few days of their current food to avoid a sudden diet change",
            "Set a house rule list with everyone in the household (furniture, feeding, doors)",
        ]),
        ("Day 1", [
            "Keep the first car ride and arrival calm and low-key",
            "Show them the water bowl and a quiet resting spot right away",
            "Take them out to the same potty spot often, and praise calmly when they go",
            "Skip the welcome party — let visitors wait a few days",
        ]),
        ("Days 2–3", [
            "Start a simple feeding and potty schedule and stick to it",
            "Begin short, positive name and hand-target training sessions",
            "Note any sniffing, hiding, or clinginess — settling in looks different for every dog",
        ]),
        ("Days 4–7", [
            "Introduce one new person or short outing at a time",
            "Book their first vet visit if it isn't already scheduled",
            "Start loose-leash walks in a quiet area before busier streets",
            "Begin crate or alone-time practice in very short sessions",
        ]),
    ],
    ("dog", "supplies"): [
        ("Feeding", [
            "Food and water bowls",
            "A few days' supply of their current food",
            "Treats for training",
            "A slow feeder if they eat quickly",
        ]),
        ("Sleeping & containment", [
            "Crate or dog bed sized for them",
            "Baby gate or exercise pen if needed",
            "Blanket or crate pad",
        ]),
        ("Walking & ID", [
            "Well-fitted collar or harness",
            "Leash",
            "ID tag with a current phone number",
            "Microchip registration confirmed and up to date",
        ]),
        ("Everyday care", [
            "Poop bags",
            "Brush suited to their coat",
            "Nail trimmer or grinder",
            "Enzymatic cleaner for accidents",
            "A few safe chew toys",
        ]),
    ],
    ("dog", "vet-visit"): [
        ("Bring with you", [
            "Any records from a shelter, rescue, or breeder",
            "A stool sample if your vet's office asks for one",
            "A list of any behaviors or symptoms you've noticed",
        ]),
        ("Questions to ask", [
            "What vaccines are due now, and what's the schedule going forward?",
            "Is a parasite or heartworm test needed?",
            "What food and feeding amount do you recommend for their age and weight?",
            "When should we talk about spay or neuter timing?",
            "What's the plan for flea, tick, and heartworm prevention?",
        ]),
        ("Bring home", [
            "A written copy of their vaccine and treatment record",
            "Next appointment date",
            "Any prescribed medication with clear dosing instructions",
        ]),
    ],
    ("dog", "pet-proofing"): [
        ("Kitchen", [
            "Store xylitol, chocolate, onions, and grapes out of reach",
            "Secure the trash can with a locking lid",
            "Tuck away dish towels and anything dangling from counters",
        ]),
        ("Living areas", [
            "Tape or hide loose cords and cables",
            "Move small chewable objects and remotes up and out of reach",
            "Check houseplants against a pet-safe plant list",
            "Secure bookshelves or furniture that could tip",
        ]),
        ("Bathroom & laundry", [
            "Keep the toilet lid down and medications in a closed cabinet",
            "Store cleaning supplies and detergent pods on a high shelf",
            "Keep the laundry hamper (socks, elastic) out of reach",
        ]),
        ("Yard & exits", [
            "Walk the fence line for gaps or digging spots",
            "Check the gate latch works and is visible to guests",
            "Remove or fence off toxic plants, mulch, or fertilizer",
        ]),
    ],

    ("cat", "first-week"): [
        ("Before they arrive", [
            "Set up one quiet base room with litter box, food, water, and a hiding spot",
            "Keep the litter box far from food and water",
            "Buy a few days of their current food to avoid a sudden switch",
            "Add a scratching post near their base room",
        ]),
        ("Day 1", [
            "Bring them straight to the base room and let them explore in their own time",
            "Skip forcing interaction — sit nearby and let them approach",
            "Keep other pets separated behind a closed door for now",
        ]),
        ("Days 2–3", [
            "Start a steady feeding schedule",
            "Watch litter box use for signs of stress or discomfort",
            "Offer a few toy options to see what sparks interest",
        ]),
        ("Days 4–7", [
            "Begin short supervised access to one more room",
            "Start slow scent-swapping if introducing another household pet",
            "Book their first vet visit if it isn't already scheduled",
        ]),
    ],
    ("cat", "supplies"): [
        ("Feeding", [
            "Food and water bowls or a fountain",
            "A few days' supply of their current food",
            "Treats for positive reinforcement",
        ]),
        ("Litter", [
            "Litter box (one per cat, plus one extra is a common guideline)",
            "Litter matching what they're used to, if known",
            "Scoop and box liners if you use them",
        ]),
        ("Comfort & enrichment", [
            "Scratching post or pad",
            "A few toys, including one wand toy for interactive play",
            "A cozy bed or blanket in their base room",
            "A carrier they can get used to, not just travel in",
        ]),
        ("Everyday care", [
            "Brush suited to their coat",
            "Nail trimmer",
            "ID tag and microchip registration confirmed and up to date",
        ]),
    ],
    ("cat", "vet-visit"): [
        ("Bring with you", [
            "Any records from a shelter, rescue, or breeder",
            "The carrier, ideally already familiar to them",
            "A list of any behaviors, appetite, or litter box changes you've noticed",
        ]),
        ("Questions to ask", [
            "What vaccines are due now, and what's the schedule going forward?",
            "Should we test for FeLV/FIV if it hasn't been done?",
            "What food and feeding amount fits their age and weight?",
            "When should we talk about spay or neuter timing?",
            "What's the plan for flea and parasite prevention?",
        ]),
        ("Bring home", [
            "A written copy of their vaccine and treatment record",
            "Next appointment date",
            "Any prescribed medication with clear dosing instructions",
        ]),
    ],
    ("cat", "pet-proofing"): [
        ("Kitchen", [
            "Store chocolate, onions, and garlic out of reach",
            "Keep the trash can covered or behind a cabinet door",
            "Turn off stove knobs or use covers if they jump on counters",
        ]),
        ("Living areas", [
            "Tape or hide loose cords and blind cords",
            "Check houseplants against a pet-safe plant list (lilies are highly toxic to cats)",
            "Cover or screen open windows — even a small gap is a risk",
            "Tuck away small objects like hair ties, string, and rubber bands",
        ]),
        ("Bathroom & laundry", [
            "Keep the toilet lid down and medications in a closed cabinet",
            "Store cleaning supplies on a high, closed shelf",
            "Check the dryer and washer before every load",
        ]),
        ("Balconies & high spots", [
            "Add secure screens to any open windows or balconies",
            "Check nothing breakable sits where they're likely to jump",
        ]),
    ],

    ("small-furry", "first-week"): [
        ("Before they arrive", [
            "Set up the enclosure in a quiet, temperature-stable spot away from drafts",
            "Add hiding spots, bedding, and a litter corner if litter-training",
            "Have hay (for rabbits and guinea pigs) ready and fresh",
            "Buy a few days of their current pellet food to avoid a sudden switch",
        ]),
        ("Day 1", [
            "Let them settle into the enclosure without handling for the first day",
            "Offer fresh hay, water, and a small amount of pellets",
            "Keep the room calm and free of loud noise",
        ]),
        ("Days 2–3", [
            "Start short, calm handling sessions at floor level",
            "Watch appetite, droppings, and activity level daily",
            "Begin a consistent feeding schedule",
        ]),
        ("Days 4–7", [
            "Offer supervised time in a safe, enclosed exercise space",
            "Introduce one new vegetable at a time to check for tolerance",
            "Book their first vet visit with an exotics-experienced vet if possible",
        ]),
    ],
    ("small-furry", "supplies"): [
        ("Habitat", [
            "Enclosure sized appropriately for the species and number of pets",
            "Bedding safe for their species (avoid cedar and pine shavings)",
            "Hide box or tunnel",
            "Litter box and pet-safe litter, if litter-training",
        ]),
        ("Feeding", [
            "Unlimited fresh hay for rabbits and guinea pigs",
            "Age-appropriate pellets",
            "Water bottle or bowl",
            "Vitamin C supplement for guinea pigs, if recommended by your vet",
        ]),
        ("Enrichment", [
            "Chew-safe wood toys",
            "Tunnels or cardboard boxes",
            "A safe grooming brush",
        ]),
        ("Everyday care", [
            "Nail trimmer sized for small pets",
            "Enclosure cleaning supplies",
            "A small, secure carrier for vet visits",
        ]),
    ],
    ("small-furry", "vet-visit"): [
        ("Bring with you", [
            "Any records from a shelter, rescue, or breeder",
            "A secure, well-ventilated carrier",
            "Notes on appetite, droppings, and activity since arrival",
        ]),
        ("Questions to ask", [
            "Is this vet experienced with rabbits, guinea pigs, or other exotics?",
            "What's an appropriate diet and hay-to-pellet ratio?",
            "Are there species-specific health checks we should schedule (teeth, for example)?",
            "When should we talk about spay or neuter timing?",
            "What are early warning signs we should watch for at home?",
        ]),
        ("Bring home", [
            "A written copy of their exam notes and any treatment plan",
            "Next appointment date",
            "Diet or husbandry adjustments to make at home",
        ]),
    ],
    ("small-furry", "pet-proofing"): [
        ("Exercise area", [
            "Remove or cover electrical cords in any play space",
            "Block gaps behind and under furniture where they could get stuck",
            "Check houseplants against a pet-safe plant list before free-roam time",
        ]),
        ("Enclosure placement", [
            "Keep the enclosure out of direct sun and away from drafts or heating vents",
            "Keep other household pets from having unsupervised access",
            "Check the enclosure has no sharp edges or wire your pet could chew",
        ]),
        ("Household hazards", [
            "Store cleaning supplies well away from the enclosure and play area",
            "Keep houseplants and floral arrangements out of free-roam areas",
            "Secure any small objects that could be chewed or swallowed",
        ]),
    ],

    ("bird", "first-week"): [
        ("Before they arrive", [
            "Set up the cage in a draft-free spot, away from the kitchen",
            "Add perches of varying width and a few safe toys",
            "Remove any non-stick cookware from the kitchen — fumes are dangerous to birds",
            "Buy a few days of their current diet to avoid a sudden switch",
        ]),
        ("Day 1", [
            "Let them settle into the cage without handling for the first day",
            "Keep the room calm and avoid loud noise or sudden movement",
            "Offer fresh food and water and note what they actually eat",
        ]),
        ("Days 2–3", [
            "Start talking softly near the cage to build familiarity",
            "Begin a consistent feeding and lights-out schedule",
            "Watch droppings, appetite, and activity level daily",
        ]),
        ("Days 4–7", [
            "Begin short, calm hand-taming sessions if they're ready",
            "Offer supervised out-of-cage time in a bird-proofed room",
            "Book their first vet visit with an avian-experienced vet if possible",
        ]),
    ],
    ("bird", "supplies"): [
        ("Habitat", [
            "Cage sized appropriately for the species, with horizontal bar spacing for climbing",
            "Several perches in different widths and textures",
            "Food and water dishes",
            "Cage cover for a consistent sleep schedule",
        ]),
        ("Feeding", [
            "Species-appropriate pellet or seed mix",
            "Fresh vegetables and fruit safe for their species",
            "Cuttlebone or mineral block",
        ]),
        ("Enrichment", [
            "A few foraging or chew-safe toys",
            "Rotating toy schedule to prevent boredom",
            "A play stand for supervised out-of-cage time",
        ]),
        ("Everyday care", [
            "Cage liner or substrate",
            "Cage cleaning supplies",
            "A small, secure travel carrier for vet visits",
        ]),
    ],
    ("bird", "vet-visit"): [
        ("Bring with you", [
            "Any records from a shelter, rescue, or breeder",
            "A secure, covered carrier for the trip",
            "Notes on droppings, appetite, and activity since arrival",
        ]),
        ("Questions to ask", [
            "Is this vet experienced with avian patients?",
            "What's an appropriate diet for their species and life stage?",
            "Should we test for common illnesses given their history?",
            "What environmental setup (light, humidity, perches) do you recommend?",
            "What are early warning signs we should watch for at home?",
        ]),
        ("Bring home", [
            "A written copy of their exam notes and any treatment plan",
            "Next appointment date",
            "Diet or habitat adjustments to make at home",
        ]),
    ],
    ("bird", "pet-proofing"): [
        ("Kitchen & air quality", [
            "Remove non-stick (PTFE) cookware and self-cleaning oven use — fumes can be fatal to birds",
            "Keep the cage out of the kitchen entirely if possible",
            "Avoid scented candles, air fresheners, and aerosol sprays near the cage",
        ]),
        ("Out-of-cage room", [
            "Cover or close windows and mirrors before free-flight time",
            "Turn off ceiling fans in the room",
            "Check houseplants against a pet-safe plant list",
            "Keep other pets out of the room during out-of-cage time",
        ]),
        ("Cage area", [
            "Keep the cage away from direct drafts and heating or cooling vents",
            "Check toys and perches for small parts that could be swallowed",
            "Keep the cage out of direct, unfiltered sunlight without shade options",
        ]),
    ],
}

# Ensure every species/category combination has content
for sp in SPECIES:
    for cat in CATEGORIES:
        assert (sp, cat) in CHECKLISTS, f"Missing content for {sp}/{cat}"
