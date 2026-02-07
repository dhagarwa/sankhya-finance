"""
S&P 500 Companies Database - Complete List with Comprehensive Data
Real S&P 500 companies with sector/industry information for intelligent ticker extraction
Based on official S&P 500 data as of 2025
"""

SP500_COMPANIES = {
    # Technology Sector
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories",
        "keywords": ["apple", "iphone", "ipad", "mac", "macbook", "technology", "consumer electronics", "smartphone", "computer", "tablet", "watch", "airpods", "software", "hardware", "innovation", "mobile", "tech giant"]
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Information Technology", 
        "industry": "Systems Software",
        "description": "Develops, licenses, and supports software, services, devices, and solutions worldwide",
        "keywords": ["microsoft", "windows", "office", "cloud", "software", "azure", "enterprise", "productivity", "operating system", "business software", "tech", "computing", "xbox", "teams", "outlook"]
    },
    "GOOGL": {
        "name": "Alphabet Inc. (Class A)",
        "sector": "Communication Services",
        "industry": "Interactive Media & Services", 
        "description": "Google's parent company providing internet search, advertising technologies, and cloud computing",
        "keywords": ["google", "alphabet", "search", "youtube", "android", "cloud", "advertising", "internet", "search engine", "digital", "technology", "ai", "artificial intelligence", "gmail", "maps"]
    },
    "GOOG": {
        "name": "Alphabet Inc. (Class C)", 
        "sector": "Communication Services",
        "industry": "Interactive Media & Services",
        "description": "Google's parent company providing internet search, advertising technologies, and cloud computing", 
        "keywords": ["google", "alphabet", "search", "youtube", "android", "cloud", "advertising", "internet", "search engine", "digital", "technology", "ai", "artificial intelligence", "gmail", "maps"]
    },
    "META": {
        "name": "Meta Platforms Inc.",
        "sector": "Communication Services",
        "industry": "Interactive Media & Services",
        "description": "Operates social networking platforms including Facebook, Instagram, WhatsApp, and metaverse technologies",
        "keywords": ["meta", "facebook", "instagram", "whatsapp", "social media", "social network", "metaverse", "virtual reality", "vr", "oculus", "digital", "social", "platform"]
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs graphics processing units (GPUs) for gaming, professional markets, and artificial intelligence",
        "keywords": ["nvidia", "gpu", "graphics", "ai", "artificial intelligence", "semiconductors", "gaming", "machine learning", "deep learning", "data center", "chips", "processors", "geforce"]
    },
    "AVGO": {
        "name": "Broadcom Inc.",
        "sector": "Information Technology", 
        "industry": "Semiconductors",
        "description": "Designs, develops, and supplies semiconductor and infrastructure software solutions",
        "keywords": ["broadcom", "semiconductors", "chips", "wireless", "networking", "infrastructure", "software", "enterprise", "communication", "technology"]
    },
    "ADBE": {
        "name": "Adobe Inc.",
        "sector": "Information Technology",
        "industry": "Application Software", 
        "description": "Provides digital media and marketing solutions through Creative Cloud and Experience Cloud",
        "keywords": ["adobe", "creative", "photoshop", "illustrator", "software", "design", "creative cloud", "digital media", "marketing", "creative software", "graphics", "publishing"]
    },
    "CRM": {
        "name": "Salesforce Inc.",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Provides customer relationship management (CRM) software and enterprise cloud computing solutions",
        "keywords": ["salesforce", "crm", "customer relationship management", "cloud", "enterprise software", "sales", "marketing", "service", "business software", "saas"]
    },
    "ORCL": {
        "name": "Oracle Corporation", 
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "Provides database software and technology, cloud engineered systems, and enterprise software products",
        "keywords": ["oracle", "database", "enterprise software", "cloud", "infrastructure", "business software", "database management", "enterprise", "technology", "software"]
    },
    "CSCO": {
        "name": "Cisco Systems Inc.",
        "sector": "Information Technology",
        "industry": "Communications Equipment",
        "description": "Designs, manufactures, and sells Internet Protocol based networking and communications products",
        "keywords": ["cisco", "networking", "communications", "internet", "infrastructure", "routers", "switches", "security", "enterprise", "network equipment", "it"]
    },
    "INTC": {
        "name": "Intel Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductors", 
        "description": "Designs and manufactures computer processors and related technologies for business and consumer markets",
        "keywords": ["intel", "processors", "semiconductors", "chips", "cpu", "microprocessors", "computing", "technology", "hardware", "computer chips"]
    },
    "AMD": {
        "name": "Advanced Micro Devices Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs and integrates processors and related technologies for servers, desktops, and mobile devices",
        "keywords": ["amd", "processors", "semiconductors", "chips", "cpu", "gpu", "computing", "technology", "gaming", "server", "ryzen", "radeon"]
    },
    "QCOM": {
        "name": "QUALCOMM Incorporated",
        "sector": "Information Technology", 
        "industry": "Semiconductors",
        "description": "Develops and commercializes digital communications products and services",
        "keywords": ["qualcomm", "wireless", "mobile", "communications", "semiconductors", "5g", "smartphone", "chips", "snapdragon", "technology"]
    },
    "TXN": {
        "name": "Texas Instruments Incorporated",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs and manufactures semiconductors and integrated circuits for various markets",
        "keywords": ["texas instruments", "semiconductors", "chips", "analog", "embedded processing", "technology", "electronics", "manufacturing"]
    },
    "AMAT": {
        "name": "Applied Materials Inc.",
        "sector": "Information Technology", 
        "industry": "Semiconductor Materials & Equipment",
        "description": "Provides manufacturing equipment, services, and software to semiconductor and display industries",
        "keywords": ["applied materials", "semiconductor equipment", "manufacturing", "technology", "equipment", "wafer", "chip manufacturing", "materials"]
    },
    "LRCX": {
        "name": "Lam Research Corporation",
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment", 
        "description": "Supplies wafer fabrication equipment and services to the semiconductor industry",
        "keywords": ["lam research", "semiconductor equipment", "wafer", "fabrication", "manufacturing", "technology", "equipment", "chip manufacturing"]
    },
    "MU": {
        "name": "Micron Technology Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Manufactures and markets memory and storage products including DRAM and NAND flash memory",
        "keywords": ["micron", "memory", "storage", "semiconductors", "dram", "nand", "flash memory", "technology", "data storage", "chips"]
    },
    "KLAC": {
        "name": "KLA Corporation", 
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment",
        "description": "Supplies process control and yield management solutions for semiconductor and related industries",
        "keywords": ["kla", "semiconductor equipment", "process control", "yield management", "technology", "manufacturing", "equipment", "testing"]
    },
    "NXPI": {
        "name": "NXP Semiconductors N.V.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Provides high-performance mixed-signal and standard product semiconductors",
        "keywords": ["nxp", "semiconductors", "automotive", "iot", "mobile", "infrastructure", "security", "chips", "technology"]
    },
    "ADI": {
        "name": "Analog Devices Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors", 
        "description": "Designs, manufactures, and markets analog, mixed-signal, and digital signal processing integrated circuits",
        "keywords": ["analog devices", "semiconductors", "analog", "signal processing", "chips", "technology", "industrial", "automotive"]
    },
    "MCHP": {
        "name": "Microchip Technology Incorporated",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Develops, manufactures, and sells specialized semiconductor products",
        "keywords": ["microchip", "semiconductors", "microcontrollers", "analog", "technology", "embedded", "chips", "automotive", "industrial"]
    },
    "ON": {
        "name": "ON Semiconductor Corporation", 
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Supplies power and signal management solutions for automotive and industrial applications",
        "keywords": ["on semiconductor", "power management", "automotive", "industrial", "semiconductors", "chips", "technology", "power"]
    },
    "SWKS": {
        "name": "Skyworks Solutions Inc.",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Designs, develops, and markets high-performance analog semiconductors",
        "keywords": ["skyworks", "semiconductors", "analog", "wireless", "mobile", "infrastructure", "chips", "technology", "communications"]
    },

    # Healthcare Sector  
    "UNH": {
        "name": "UnitedHealth Group Incorporated",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Operates as a diversified health care company providing health benefits and health services",
        "keywords": ["unitedhealth", "health insurance", "healthcare", "medical insurance", "health benefits", "health services", "managed care", "insurance", "medical"]
    },
    "JNJ": {
        "name": "Johnson & Johnson",
        "sector": "Health Care", 
        "industry": "Pharmaceuticals",
        "description": "Researches, develops, manufactures, and sells pharmaceuticals, medical devices, and consumer products",
        "keywords": ["johnson", "jnj", "pharmaceutical", "healthcare", "medical", "drugs", "medicine", "medical devices", "consumer health", "pharmaceuticals"]
    },
    "PFE": {
        "name": "Pfizer Inc.",
        "sector": "Health Care",
        "industry": "Pharmaceuticals", 
        "description": "Develops, manufactures, and commercializes medicines and vaccines",
        "keywords": ["pfizer", "pharmaceutical", "healthcare", "vaccine", "drugs", "medicine", "covid", "biopharma", "research", "medical"]
    },
    "ABT": {
        "name": "Abbott Laboratories",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Develops, manufactures, and sells health care products including diagnostics, medical devices, nutrition, and pharmaceuticals",
        "keywords": ["abbott", "healthcare", "medical devices", "diagnostics", "nutrition", "pharmaceuticals", "medical", "health", "testing", "infant formula"]
    },
    "TMO": {
        "name": "Thermo Fisher Scientific Inc.",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Provides analytical instruments, equipment, reagents, and consumables for research and diagnostics",
        "keywords": ["thermo fisher", "life sciences", "analytical instruments", "research", "diagnostics", "laboratory", "scientific", "biotechnology", "healthcare"]
    },
    "DHR": {
        "name": "Danaher Corporation",
        "sector": "Health Care",
        "industry": "Health Care Equipment", 
        "description": "Designs, manufactures, and markets medical, industrial, and commercial products and services",
        "keywords": ["danaher", "healthcare", "medical", "life sciences", "diagnostics", "biotechnology", "industrial", "scientific", "instruments"]
    },
    "BMY": {
        "name": "Bristol-Myers Squibb Company",
        "sector": "Health Care",
        "industry": "Pharmaceuticals",
        "description": "Discovers, develops, licenses, manufactures, and markets pharmaceutical products",
        "keywords": ["bristol myers squibb", "pharmaceutical", "drugs", "medicine", "oncology", "immunology", "healthcare", "biopharma", "cancer", "research"]
    },
    "ABBV": {
        "name": "AbbVie Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Researches, develops, and commercializes advanced therapies for complex and serious diseases",
        "keywords": ["abbvie", "biotechnology", "pharmaceutical", "immunology", "oncology", "neuroscience", "drugs", "medicine", "healthcare", "humira"]
    },
    "LLY": {
        "name": "Eli Lilly and Company",
        "sector": "Health Care",
        "industry": "Pharmaceuticals", 
        "description": "Discovers, develops, manufactures, and markets human pharmaceuticals worldwide",
        "keywords": ["eli lilly", "pharmaceutical", "diabetes", "oncology", "immunology", "neurodegenerative", "drugs", "medicine", "healthcare", "insulin"]
    },
    "GILD": {
        "name": "Gilead Sciences Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Researches, develops, and commercializes medicines in areas of unmet medical need",
        "keywords": ["gilead", "biotechnology", "antiviral", "hiv", "hepatitis", "oncology", "pharmaceutical", "drugs", "medicine", "healthcare"]
    },
    "AMGN": {
        "name": "Amgen Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology", 
        "description": "Discovers, develops, manufactures, and delivers human therapeutics",
        "keywords": ["amgen", "biotechnology", "therapeutics", "oncology", "cardiovascular", "bone health", "inflammatory", "drugs", "medicine", "healthcare"]
    },
    "VRTX": {
        "name": "Vertex Pharmaceuticals Incorporated",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Engages in developing and commercializing therapies for treating serious diseases",
        "keywords": ["vertex", "biotechnology", "cystic fibrosis", "rare diseases", "pharmaceutical", "drugs", "medicine", "healthcare", "specialty"]
    },
    "REGN": {
        "name": "Regeneron Pharmaceuticals Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Discovers, invents, develops, manufactures, and commercializes medicines",
        "keywords": ["regeneron", "biotechnology", "pharmaceutical", "immunology", "oncology", "ophthalmology", "drugs", "medicine", "healthcare", "antibodies"]
    },
    "MRNA": {
        "name": "Moderna Inc.",
        "sector": "Health Care", 
        "industry": "Biotechnology",
        "description": "Develops messenger RNA therapeutics and vaccines",
        "keywords": ["moderna", "mrna", "vaccines", "covid", "biotechnology", "pharmaceutical", "messenger rna", "immunology", "healthcare", "vaccines"]
    },
    "BIIB": {
        "name": "Biogen Inc.",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Discovers, develops, and delivers therapies for neurological and neurodegenerative diseases",
        "keywords": ["biogen", "biotechnology", "neurology", "multiple sclerosis", "alzheimer", "neurological", "pharmaceutical", "drugs", "medicine", "healthcare"]
    },
    "ISRG": {
        "name": "Intuitive Surgical Inc.",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Develops, manufactures, and markets robotic products for minimally invasive surgery",
        "keywords": ["intuitive surgical", "robotic surgery", "medical devices", "surgery", "minimally invasive", "da vinci", "healthcare", "surgical", "robotics"]
    },

    # Financial Sector
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides financial services including investment banking, financial services for consumers and small businesses, and asset management",
        "keywords": ["jpmorgan", "chase", "bank", "financial", "investment banking", "banking", "financial services", "loans", "credit cards", "wealth management"]
    },
    "BAC": {
        "name": "Bank of America Corporation",
        "sector": "Financials",
        "industry": "Diversified Banks", 
        "description": "Provides banking and financial products and services for individuals, small and middle-market businesses, and large corporations",
        "keywords": ["bank of america", "bank", "financial", "banking", "loans", "credit cards", "wealth management", "merrill lynch", "financial services"]
    },
    "WFC": {
        "name": "Wells Fargo & Company",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides banking, insurance, investments, mortgage, and consumer and commercial finance",
        "keywords": ["wells fargo", "bank", "financial", "banking", "loans", "mortgage", "financial services", "commercial banking", "consumer banking"]
    },
    "GS": {
        "name": "The Goldman Sachs Group Inc.",
        "sector": "Financials",
        "industry": "Investment Banking & Brokerage",
        "description": "Provides investment banking, securities, and investment management services to corporations, financial institutions, governments, and individuals",
        "keywords": ["goldman sachs", "investment banking", "financial", "securities", "investment management", "trading", "wealth management", "asset management"]
    },
    "MS": {
        "name": "Morgan Stanley",
        "sector": "Financials", 
        "industry": "Investment Banking & Brokerage",
        "description": "Provides investment banking, securities, wealth management, and investment management services",
        "keywords": ["morgan stanley", "investment banking", "financial", "securities", "wealth management", "asset management", "trading", "financial advisory"]
    },
    "C": {
        "name": "Citigroup Inc.",
        "sector": "Financials",
        "industry": "Diversified Banks",
        "description": "Provides financial products and services including banking, lending, and investment services",
        "keywords": ["citigroup", "citi", "bank", "financial", "banking", "credit cards", "loans", "global banking", "financial services"]
    },
    "AXP": {
        "name": "American Express Company",
        "sector": "Financials",
        "industry": "Consumer Finance",
        "description": "Provides charge and credit payment card products and travel-related services worldwide",
        "keywords": ["american express", "amex", "credit cards", "charge cards", "payments", "travel", "financial services", "merchant services"]
    },
    "BLK": {
        "name": "BlackRock Inc.",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks", 
        "description": "Provides investment management, risk management, and advisory services",
        "keywords": ["blackrock", "asset management", "investment management", "etf", "ishares", "financial", "fund management", "institutional"]
    },
    "SCHW": {
        "name": "The Charles Schwab Corporation",
        "sector": "Financials",
        "industry": "Investment Banking & Brokerage",
        "description": "Provides wealth management, securities brokerage, and banking services",
        "keywords": ["charles schwab", "schwab", "brokerage", "wealth management", "trading", "financial", "investment", "retirement", "banking"]
    },
    "COF": {
        "name": "Capital One Financial Corporation",
        "sector": "Financials",
        "industry": "Consumer Finance",
        "description": "Provides banking services, lending products, and deposit products",
        "keywords": ["capital one", "bank", "credit cards", "financial", "banking", "loans", "consumer finance", "digital banking"]
    },
    "USB": {
        "name": "U.S. Bancorp",
        "sector": "Financials", 
        "industry": "Diversified Banks",
        "description": "Provides banking, investment, mortgage, trust, and payment services",
        "keywords": ["us bank", "bancorp", "bank", "financial", "banking", "loans", "financial services", "payment services"]
    },
    "PNC": {
        "name": "The PNC Financial Services Group Inc.",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Provides retail and business banking, residential mortgage, and corporate and institutional banking",
        "keywords": ["pnc", "bank", "financial", "banking", "loans", "mortgage", "regional bank", "financial services"]
    },
    "TFC": {
        "name": "Truist Financial Corporation",
        "sector": "Financials",
        "industry": "Regional Banks", 
        "description": "Provides banking and trust services for consumer and commercial clients",
        "keywords": ["truist", "bank", "financial", "banking", "loans", "trust", "regional bank", "financial services", "bb&t", "suntrust"]
    },

    # Consumer Discretionary Sector - Automotive
    "TSLA": {
        "name": "Tesla Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Automobiles",
        "description": "Designs, develops, manufactures, and sells electric vehicles and energy generation and storage systems",
        "keywords": ["tesla", "electric vehicle", "ev", "car", "automotive", "electric car", "model s", "model 3", "model x", "model y", "elon musk", "battery", "solar", "autopilot"]
    },
    "F": {
        "name": "Ford Motor Company",
        "sector": "Consumer Discretionary",
        "industry": "Automobiles",
        "description": "Designs, manufactures, markets, and services cars, trucks, and SUVs worldwide",
        "keywords": ["ford", "car", "automotive", "vehicle", "truck", "manufacturer", "mustang", "f-150", "electric vehicle", "suv"]
    },
    "GM": {
        "name": "General Motors Company",
        "sector": "Consumer Discretionary", 
        "industry": "Automobiles",
        "description": "Designs, builds, and sells cars, trucks, and automobile parts worldwide",
        "keywords": ["general motors", "gm", "car", "automotive", "vehicle", "chevrolet", "cadillac", "buick", "gmc", "electric vehicle", "truck"]
    },

    # Consumer Discretionary - Retail
    "AMZN": {
        "name": "Amazon.com Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Broadline Retail",
        "description": "Operates online marketplace and provides cloud computing services",
        "keywords": ["amazon", "ecommerce", "retail", "cloud", "aws", "online shopping", "marketplace", "prime", "alexa", "web services"]
    },
    "HD": {
        "name": "The Home Depot Inc.",
        "sector": "Consumer Discretionary", 
        "industry": "Home Improvement Retail",
        "description": "Operates retail stores selling building materials, home improvement, and lawn and garden products",
        "keywords": ["home depot", "retail", "home improvement", "hardware", "diy", "building materials", "construction", "tools", "garden"]
    },
    "LOW": {
        "name": "Lowe's Companies Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Home Improvement Retail",
        "description": "Operates home improvement retail stores offering products for maintenance, repair, remodeling, and decorating",
        "keywords": ["lowes", "retail", "home improvement", "hardware", "diy", "building materials", "construction", "tools", "garden", "appliances"]
    },
    "TGT": {
        "name": "Target Corporation",
        "sector": "Consumer Discretionary",
        "industry": "General Merchandise Stores",
        "description": "Operates general merchandise stores offering food and general merchandise",
        "keywords": ["target", "retail", "general merchandise", "discount retail", "department store", "grocery", "clothing", "home goods"]
    },
    "WMT": {
        "name": "Walmart Inc.",
        "sector": "Consumer Staples", 
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Operates retail stores, restaurants, and e-commerce websites in various formats worldwide",
        "keywords": ["walmart", "retail", "grocery", "supermarket", "consumer goods", "discount retail", "supercenter", "ecommerce"]
    },
    "COST": {
        "name": "Costco Wholesale Corporation",
        "sector": "Consumer Staples",
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Operates membership warehouses offering branded and private-label products in bulk quantities",
        "keywords": ["costco", "wholesale", "warehouse", "membership", "bulk", "retail", "grocery", "consumer goods"]
    },
    "TJX": {
        "name": "The TJX Companies Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Apparel Retail", 
        "description": "Operates off-price apparel and home fashions retail stores",
        "keywords": ["tjx", "tj maxx", "retail", "clothing", "apparel", "fashion", "discount retail", "marshalls", "home goods"]
    },

    # Consumer Discretionary - Restaurants
    "MCD": {
        "name": "McDonald's Corporation",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates and franchises McDonald's restaurants worldwide",
        "keywords": ["mcdonalds", "fast food", "restaurant", "franchise", "quick service", "food", "dining", "hamburger", "global"]
    },
    "SBUX": {
        "name": "Starbucks Corporation",
        "sector": "Consumer Discretionary", 
        "industry": "Restaurants",
        "description": "Roasts, markets, and retails specialty coffee worldwide",
        "keywords": ["starbucks", "coffee", "cafe", "beverage", "restaurant", "retail", "specialty coffee", "food service"]
    },
    "CMG": {
        "name": "Chipotle Mexican Grill Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates fast-casual Mexican restaurant chain",
        "keywords": ["chipotle", "mexican", "fast casual", "restaurant", "burrito", "food", "dining", "quick service"]
    },
    "YUM": {
        "name": "Yum! Brands Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Operates restaurant chains including KFC, Pizza Hut, and Taco Bell",
        "keywords": ["yum brands", "kfc", "pizza hut", "taco bell", "fast food", "restaurant", "franchise", "quick service", "food"]
    },

    # Energy Sector
    "XOM": {
        "name": "Exxon Mobil Corporation", 
        "sector": "Energy",
        "industry": "Integrated Oil & Gas",
        "description": "Engages in the exploration and production of crude oil and natural gas",
        "keywords": ["exxon", "oil", "gas", "energy", "petroleum", "fossil fuel", "refining", "chemicals", "exploration", "drilling"]
    },
    "CVX": {
        "name": "Chevron Corporation",
        "sector": "Energy",
        "industry": "Integrated Oil & Gas",
        "description": "Engages in integrated energy, chemicals, and petroleum operations worldwide",
        "keywords": ["chevron", "oil", "gas", "energy", "petroleum", "refining", "chemicals", "exploration", "drilling", "fuel"]
    },
    "COP": {
        "name": "ConocoPhillips",
        "sector": "Energy", 
        "industry": "Oil & Gas Exploration & Production",
        "description": "Explores for, produces, transports, and markets crude oil, bitumen, natural gas, and liquefied natural gas",
        "keywords": ["conocophillips", "oil", "gas", "exploration", "production", "energy", "petroleum", "drilling", "lng"]
    },
    "EOG": {
        "name": "EOG Resources Inc.",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Explores for, develops, produces, and markets crude oil and natural gas",
        "keywords": ["eog", "oil", "gas", "exploration", "production", "energy", "petroleum", "drilling", "shale", "unconventional"]
    },
    "SLB": {
        "name": "Schlumberger Limited",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services", 
        "description": "Provides technology for reservoir characterization, drilling, production, and processing to oil and gas industry",
        "keywords": ["schlumberger", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "technology", "services"]
    },
    "HAL": {
        "name": "Halliburton Company",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services",
        "description": "Provides products and services to the energy industry for upstream oil and gas exploration and production",
        "keywords": ["halliburton", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "completion", "services"]
    },
    "BKR": {
        "name": "Baker Hughes Company",
        "sector": "Energy",
        "industry": "Oil & Gas Equipment & Services",
        "description": "Provides oilfield services, products, technology, and systems to oil and natural gas industry",
        "keywords": ["baker hughes", "oilfield services", "drilling", "oil", "gas", "energy", "equipment", "technology", "industrial"]
    },

    # Utilities Sector
    "NEE": {
        "name": "NextEra Energy Inc.", 
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Generates, transmits, distributes, and sells electric power to retail and wholesale customers",
        "keywords": ["nextera", "utility", "electric", "power", "renewable energy", "solar", "wind", "electricity", "energy", "clean energy"]
    },
    "SO": {
        "name": "The Southern Company",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Generates, transmits, and distributes electricity through its subsidiaries",
        "keywords": ["southern company", "utility", "electric", "power", "electricity", "energy", "generation", "transmission", "distribution"]
    },
    "DUK": {
        "name": "Duke Energy Corporation",
        "sector": "Utilities",
        "industry": "Electric Utilities", 
        "description": "Operates as an energy company providing electricity to customers in the United States",
        "keywords": ["duke energy", "utility", "electric", "power", "electricity", "energy", "generation", "natural gas", "renewable"]
    },
    "D": {
        "name": "Dominion Energy Inc.",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Produces and distributes energy including natural gas and electricity",
        "keywords": ["dominion", "utility", "electric", "natural gas", "power", "electricity", "energy", "generation", "distribution"]
    },
    "AEP": {
        "name": "American Electric Power Company Inc.",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Operates as a public electric utility company generating, transmitting, and distributing electric power",
        "keywords": ["american electric power", "aep", "utility", "electric", "power", "electricity", "energy", "transmission", "generation"]
    },

    # Consumer Staples Sector
    "PG": {
        "name": "The Procter & Gamble Company", 
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Provides branded consumer packaged goods to consumers worldwide",
        "keywords": ["procter gamble", "consumer goods", "household products", "personal care", "cleaning", "tide", "pampers", "gillette", "crest", "consumer staples"]
    },
    "KO": {
        "name": "The Coca-Cola Company",
        "sector": "Consumer Staples",
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Manufactures, markets, and sells nonalcoholic beverage concentrates and syrups worldwide",
        "keywords": ["coca cola", "coke", "beverages", "soft drinks", "non-alcoholic", "consumer staples", "drinks", "global", "brand"]
    },
    "PEP": {
        "name": "PepsiCo Inc.",
        "sector": "Consumer Staples", 
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Manufactures, markets, distributes, and sells beverages, food, and snacks worldwide",
        "keywords": ["pepsi", "pepsico", "beverages", "soft drinks", "snacks", "food", "frito lay", "quaker", "consumer staples"]
    },
    "CL": {
        "name": "Colgate-Palmolive Company",
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Manufactures and markets consumer products worldwide including oral care, personal care, home care, and pet nutrition",
        "keywords": ["colgate", "palmolive", "oral care", "toothpaste", "personal care", "household products", "consumer staples", "hygiene"]
    },
    "KMB": {
        "name": "Kimberly-Clark Corporation",
        "sector": "Consumer Staples",
        "industry": "Household Products", 
        "description": "Manufactures and markets personal care and consumer tissue products worldwide",
        "keywords": ["kimberly clark", "tissue", "personal care", "kleenex", "huggies", "scott", "household products", "consumer staples", "hygiene"]
    },

    # Industrial Sector
    "CAT": {
        "name": "Caterpillar Inc.",
        "sector": "Industrials",
        "industry": "Construction Machinery & Heavy Transportation Equipment",
        "description": "Manufactures construction and mining equipment, diesel and natural gas engines, industrial gas turbines, and diesel-electric locomotives",
        "keywords": ["caterpillar", "construction", "mining", "equipment", "machinery", "heavy equipment", "industrial", "engines", "manufacturing"]
    },
    "BA": {
        "name": "The Boeing Company",
        "sector": "Industrials", 
        "industry": "Aerospace & Defense",
        "description": "Designs, develops, manufactures, and sells commercial and military aircraft worldwide",
        "keywords": ["boeing", "aerospace", "aircraft", "defense", "commercial aviation", "military", "737", "777", "787", "manufacturing"]
    },
    "GE": {
        "name": "GE Aerospace",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Provides jet engines, components, and integrated systems for commercial and military aircraft",
        "keywords": ["ge", "general electric", "aerospace", "jet engines", "aircraft", "defense", "aviation", "industrial", "manufacturing"]
    },
    "RTX": {
        "name": "RTX Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense", 
        "description": "Provides systems and services for the commercial aerospace, defense, and other markets",
        "keywords": ["rtx", "raytheon", "aerospace", "defense", "aircraft", "engines", "pratt whitney", "collins", "military"]
    },
    "LMT": {
        "name": "Lockheed Martin Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Researches, designs, develops, manufactures, integrates, and sustains technology systems and products",
        "keywords": ["lockheed martin", "defense", "aerospace", "military", "missile", "space", "government", "contractor"]
    },
    "NOC": {
        "name": "Northrop Grumman Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense", 
        "description": "Operates as an aerospace and defense company providing systems and technologies",
        "keywords": ["northrop grumman", "defense", "aerospace", "military", "space", "cyber", "government", "contractor"]
    },
    "GD": {
        "name": "General Dynamics Corporation",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Operates as an aerospace and defense company providing business aviation, ship construction, land combat systems, and information technology",
        "keywords": ["general dynamics", "defense", "aerospace", "military", "shipbuilding", "combat systems", "gulfstream", "contractor"]
    },
    "UNP": {
        "name": "Union Pacific Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation", 
        "description": "Operates railroad system in the western United States",
        "keywords": ["union pacific", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo"]
    },
    "CSX": {
        "name": "CSX Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation",
        "description": "Provides rail-based freight transportation services including traditional rail service and intermodal container and trailer transport",
        "keywords": ["csx", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo", "intermodal"]
    },
    "NSC": {
        "name": "Norfolk Southern Corporation",
        "sector": "Industrials",
        "industry": "Rail Transportation",
        "description": "Operates as a freight railroad company providing rail transportation services",
        "keywords": ["norfolk southern", "railroad", "rail", "transportation", "freight", "logistics", "shipping", "cargo"]
    },

    # Materials Sector
    "LIN": {
        "name": "Linde plc", 
        "sector": "Materials",
        "industry": "Industrial Gases",
        "description": "Operates as an industrial gas company serving customers in healthcare, petroleum refining, manufacturing, food, beverage carbonation, fiber-optics, steel making, aerospace, and other industries",
        "keywords": ["linde", "industrial gases", "chemicals", "materials", "manufacturing", "healthcare", "oxygen", "nitrogen", "hydrogen"]
    },
    "APD": {
        "name": "Air Products and Chemicals Inc.",
        "sector": "Materials",
        "industry": "Industrial Gases",
        "description": "Provides atmospheric gases, process and specialty gases, equipment, and services worldwide",
        "keywords": ["air products", "industrial gases", "chemicals", "materials", "hydrogen", "oxygen", "nitrogen", "manufacturing"]
    },
    "SHW": {
        "name": "The Sherwin-Williams Company",
        "sector": "Materials", 
        "industry": "Specialty Chemicals",
        "description": "Develops, manufactures, distributes, and sells paints, coatings, and related products worldwide",
        "keywords": ["sherwin williams", "paint", "coatings", "materials", "construction", "automotive", "specialty chemicals", "architectural"]
    },
    "ECL": {
        "name": "Ecolab Inc.",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "Provides water, hygiene, and energy technologies and services worldwide",
        "keywords": ["ecolab", "water treatment", "hygiene", "cleaning", "specialty chemicals", "materials", "industrial", "food safety"]
    },
    "DD": {
        "name": "DuPont de Nemours Inc.",
        "sector": "Materials",
        "industry": "Specialty Chemicals", 
        "description": "Provides technology-based materials, ingredients, and solutions in electronics, transportation, construction, water, healthcare, and worker safety",
        "keywords": ["dupont", "specialty chemicals", "materials", "electronics", "construction", "safety", "innovation", "chemicals"]
    },
    "DOW": {
        "name": "Dow Inc.",
        "sector": "Materials",
        "industry": "Commodity Chemicals",
        "description": "Provides chemical technology and solutions, and manufactures and sells chemical products",
        "keywords": ["dow", "chemicals", "materials", "plastics", "manufacturing", "industrial", "commodity chemicals", "chemical products"]
    },

    # Real Estate Sector
    "PLD": {
        "name": "Prologis Inc.",
        "sector": "Real Estate", 
        "industry": "Industrial REITs",
        "description": "Operates as a real estate investment trust that owns and develops logistics facilities worldwide",
        "keywords": ["prologis", "real estate", "reit", "logistics", "warehouses", "industrial", "distribution", "ecommerce", "fulfillment"]
    },
    "AMT": {
        "name": "American Tower Corporation",
        "sector": "Real Estate",
        "industry": "Telecom Tower REITs",
        "description": "Owns and operates multitenant communications real estate including wireless and broadcast towers",
        "keywords": ["american tower", "cell towers", "telecommunications", "wireless", "real estate", "reit", "infrastructure", "communications"]
    },
    "CCI": {
        "name": "Crown Castle Inc.",
        "sector": "Real Estate",
        "industry": "Telecom Tower REITs", 
        "description": "Owns, operates, and leases wireless infrastructure including cell towers and small cells",
        "keywords": ["crown castle", "cell towers", "telecommunications", "wireless", "real estate", "reit", "infrastructure", "small cells"]
    },
    "EQIX": {
        "name": "Equinix Inc.",
        "sector": "Real Estate",
        "industry": "Specialized REITs",
        "description": "Operates data centers that provide colocation and interconnection services worldwide",
        "keywords": ["equinix", "data centers", "colocation", "cloud", "internet", "real estate", "reit", "interconnection", "digital infrastructure"]
    },
    "DLR": {
        "name": "Digital Realty Trust Inc.",
        "sector": "Real Estate",
        "industry": "Specialized REITs",
        "description": "Owns, acquires, develops, and manages data centers worldwide",
        "keywords": ["digital realty", "data centers", "cloud", "internet", "real estate", "reit", "digital infrastructure", "colocation"]
    },
    "SPG": {
        "name": "Simon Property Group Inc.", 
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Operates as a retail real estate investment trust that owns, develops, and manages retail real estate properties",
        "keywords": ["simon property", "shopping malls", "retail", "real estate", "reit", "commercial", "shopping centers", "outlet"]
    },

    # Communication Services Sector
    "VZ": {
        "name": "Verizon Communications Inc.",
        "sector": "Communication Services",
        "industry": "Integrated Telecommunication Services",
        "description": "Provides communications, technology, information, and entertainment products and services to consumers, businesses, and governmental entities",
        "keywords": ["verizon", "telecommunications", "wireless", "mobile", "phone", "internet", "5g", "communications", "telecom"]
    },
    "T": {
        "name": "AT&T Inc.", 
        "sector": "Communication Services",
        "industry": "Integrated Telecommunication Services",
        "description": "Provides telecommunications, media, and technology services worldwide",
        "keywords": ["att", "at&t", "telecommunications", "wireless", "mobile", "phone", "internet", "directv", "communications", "telecom"]
    },
    "TMUS": {
        "name": "T-Mobile US Inc.",
        "sector": "Communication Services",
        "industry": "Wireless Telecommunication Services",
        "description": "Provides mobile communications services including voice, messaging, and data services",
        "keywords": ["t-mobile", "wireless", "mobile", "phone", "telecommunications", "5g", "cellular", "communications", "sprint"]
    },
    "CMCSA": {
        "name": "Comcast Corporation",
        "sector": "Communication Services",
        "industry": "Cable & Satellite", 
        "description": "Operates as a media and technology company providing cable communications, media, and technology products and services",
        "keywords": ["comcast", "cable", "internet", "media", "broadband", "nbc", "universal", "xfinity", "communications"]
    },
    "CHTR": {
        "name": "Charter Communications Inc.",
        "sector": "Communication Services",
        "industry": "Cable & Satellite",
        "description": "Provides cable services to residential and commercial customers including video, internet, and voice services",
        "keywords": ["charter", "spectrum", "cable", "internet", "communications", "broadband", "video", "voice"]
    },
    "DIS": {
        "name": "The Walt Disney Company",
        "sector": "Communication Services",
        "industry": "Entertainment", 
        "description": "Operates as an entertainment company providing content through various platforms including theme parks, resorts, media networks, and streaming services",
        "keywords": ["disney", "entertainment", "media", "theme parks", "movies", "streaming", "espn", "abc", "disney+", "content"]
    },
    "NFLX": {
        "name": "Netflix Inc.",
        "sector": "Communication Services",
        "industry": "Entertainment",
        "description": "Provides entertainment services with original and licensed content across a wide variety of genres and languages to worldwide audience",
        "keywords": ["netflix", "streaming", "entertainment", "media", "movies", "tv shows", "content", "video", "subscription"]
    },

    # Payment/Fintech
    "V": {
        "name": "Visa Inc.",
        "sector": "Financials", 
        "industry": "Transaction & Payment Processing Services",
        "description": "Operates payment processing network that enables authorization, clearing, and settlement of payment transactions worldwide",
        "keywords": ["visa", "payments", "credit cards", "debit cards", "payment processing", "financial", "transactions", "fintech"]
    },
    "MA": {
        "name": "Mastercard Incorporated",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Provides payment processing services and technology to connect consumers, financial institutions, merchants, governments, and businesses worldwide",
        "keywords": ["mastercard", "payments", "credit cards", "debit cards", "payment processing", "financial", "transactions", "fintech"]
    },
    "PYPL": {
        "name": "PayPal Holdings Inc.",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services", 
        "description": "Operates technology platform that enables digital and mobile payments and facilitates commerce and monetization",
        "keywords": ["paypal", "digital payments", "online payments", "fintech", "mobile payments", "venmo", "ecommerce", "financial technology"]
    },

    # Insurance
    "BRK.B": {
        "name": "Berkshire Hathaway Inc.",
        "sector": "Financials",
        "industry": "Multi-Sector Holdings",
        "description": "Operates as a holding company owning subsidiaries engaged in insurance and reinsurance, freight rail transportation, energy generation and distribution, manufacturing, and retailing",
        "keywords": ["berkshire hathaway", "warren buffett", "insurance", "conglomerate", "holding company", "geico", "bnsf", "financial", "investment"]
    },
    "PGR": {
        "name": "The Progressive Corporation", 
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides personal and commercial auto insurance, and other specialty property-casualty insurance and related services",
        "keywords": ["progressive", "auto insurance", "car insurance", "property casualty", "insurance", "financial", "vehicle insurance"]
    },
    "ALL": {
        "name": "The Allstate Corporation",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides property and casualty insurance and life insurance products to customers in the United States and Canada",
        "keywords": ["allstate", "auto insurance", "home insurance", "property casualty", "insurance", "financial", "life insurance"]
    },
    "CB": {
        "name": "Chubb Limited",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance", 
        "description": "Provides insurance and reinsurance products worldwide including commercial and personal property and casualty insurance",
        "keywords": ["chubb", "insurance", "property casualty", "commercial insurance", "reinsurance", "financial", "specialty insurance"]
    },
    "TRV": {
        "name": "The Travelers Companies Inc.",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Provides personal and commercial property and casualty insurance products and services",
        "keywords": ["travelers", "insurance", "property casualty", "commercial insurance", "auto insurance", "financial", "business insurance"]
    },
    "AIG": {
        "name": "American International Group Inc.",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance", 
        "description": "Provides insurance products and services for commercial, institutional, and individual customers",
        "keywords": ["aig", "american international group", "insurance", "commercial insurance", "life insurance", "financial", "global insurance"]
    },
    "MET": {
        "name": "MetLife Inc.",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Provides insurance, employee benefits, and asset management services worldwide",
        "keywords": ["metlife", "life insurance", "employee benefits", "insurance", "financial", "retirement", "group benefits"]
    },
    "PRU": {
        "name": "Prudential Financial Inc.",
        "sector": "Financials",
        "industry": "Life & Health Insurance", 
        "description": "Provides insurance, investment management, and other financial products and services",
        "keywords": ["prudential", "life insurance", "financial", "investment management", "retirement", "insurance", "asset management"]
    },
    "AFL": {
        "name": "Aflac Incorporated",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Provides supplemental health and life insurance products",
        "keywords": ["aflac", "supplemental insurance", "health insurance", "life insurance", "insurance", "financial", "duck", "worksite"]
    },
    # =========================================================================
    # Additional S&P 500 Companies (379 companies added to complete the index)
    # Sourced from official S&P 500 constituent list
    # =========================================================================
    # Information Technology (additional)
    "ACN": {
        "name": "Accenture",
        "sector": "Information Technology",
        "industry": "IT Consulting & Other Services",
        "description": "Accenture - IT Consulting & Other Services",
        "keywords": ["accenture", "consulting", "other", "services"]
    },
    "ADSK": {
        "name": "Autodesk",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Autodesk - Application Software",
        "keywords": ["autodesk", "application", "software"]
    },
    "AKAM": {
        "name": "Akamai Technologies",
        "sector": "Information Technology",
        "industry": "Internet Services & Infrastructure",
        "description": "Akamai Technologies - Internet Services & Infrastructure",
        "keywords": ["akamai", "technologies", "internet", "services", "infrastructure"]
    },
    "ANET": {
        "name": "Arista Networks",
        "sector": "Information Technology",
        "industry": "Communications Equipment",
        "description": "Arista Networks - Communications Equipment",
        "keywords": ["arista", "networks", "communications", "equipment"]
    },
    "APH": {
        "name": "Amphenol",
        "sector": "Information Technology",
        "industry": "Electronic Components",
        "description": "Amphenol - Electronic Components",
        "keywords": ["amphenol", "electronic", "components"]
    },
    "CDNS": {
        "name": "Cadence Design Systems",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Cadence Design Systems - Application Software",
        "keywords": ["cadence", "design", "systems", "application", "software"]
    },
    "CDW": {
        "name": "CDW Corporation",
        "sector": "Information Technology",
        "industry": "Technology Distributors",
        "description": "CDW Corporation - Technology Distributors",
        "keywords": ["cdw", "oration", "technology", "distributors"]
    },
    "CRWD": {
        "name": "CrowdStrike",
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "CrowdStrike - Systems Software",
        "keywords": ["crowdstrike", "systems", "software"]
    },
    "CTSH": {
        "name": "Cognizant",
        "sector": "Information Technology",
        "industry": "IT Consulting & Other Services",
        "description": "Cognizant - IT Consulting & Other Services",
        "keywords": ["gnizant", "consulting", "other", "services"]
    },
    "DDOG": {
        "name": "Datadog",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Datadog - Application Software",
        "keywords": ["datadog", "application", "software"]
    },
    "DELL": {
        "name": "Dell Technologies",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Dell Technologies - Technology Hardware, Storage & Peripherals",
        "keywords": ["dell", "technologies", "technology", "hardware", "storage", "peripherals"]
    },
    "ENPH": {
        "name": "Enphase Energy",
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment",
        "description": "Enphase Energy - Semiconductor Materials & Equipment",
        "keywords": ["enphase", "energy", "semiconductor", "materials", "equipment"]
    },
    "EPAM": {
        "name": "EPAM Systems",
        "sector": "Information Technology",
        "industry": "IT Consulting & Other Services",
        "description": "EPAM Systems - IT Consulting & Other Services",
        "keywords": ["epam", "systems", "consulting", "other", "services"]
    },
    "FFIV": {
        "name": "F5, Inc.",
        "sector": "Information Technology",
        "industry": "Communications Equipment",
        "description": "F5, Inc. - Communications Equipment",
        "keywords": ["communications", "equipment"]
    },
    "FICO": {
        "name": "Fair Isaac",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Fair Isaac - Application Software",
        "keywords": ["fair", "isaac", "application", "software"]
    },
    "FSLR": {
        "name": "First Solar",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "First Solar - Semiconductors",
        "keywords": ["first", "solar", "semiconductors"]
    },
    "FTNT": {
        "name": "Fortinet",
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "Fortinet - Systems Software",
        "keywords": ["fortinet", "systems", "software"]
    },
    "GDDY": {
        "name": "GoDaddy",
        "sector": "Information Technology",
        "industry": "Internet Services & Infrastructure",
        "description": "GoDaddy - Internet Services & Infrastructure",
        "keywords": ["godaddy", "internet", "services", "infrastructure"]
    },
    "GEN": {
        "name": "Gen Digital",
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "Gen Digital - Systems Software",
        "keywords": ["gen", "digital", "systems", "software"]
    },
    "GLW": {
        "name": "Corning Inc.",
        "sector": "Information Technology",
        "industry": "Electronic Components",
        "description": "Corning Inc. - Electronic Components",
        "keywords": ["rning", "electronic", "components"]
    },
    "HPE": {
        "name": "Hewlett Packard Enterprise",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Hewlett Packard Enterprise - Technology Hardware, Storage & Peripherals",
        "keywords": ["hewlett", "packard", "enterprise", "technology", "hardware", "storage", "peripherals"]
    },
    "HPQ": {
        "name": "HP Inc.",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "HP Inc. - Technology Hardware, Storage & Peripherals",
        "keywords": ["technology", "hardware", "storage", "peripherals"]
    },
    "IBM": {
        "name": "IBM",
        "sector": "Information Technology",
        "industry": "IT Consulting & Other Services",
        "description": "IBM - IT Consulting & Other Services",
        "keywords": ["ibm", "consulting", "other", "services"]
    },
    "INTU": {
        "name": "Intuit",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Intuit - Application Software",
        "keywords": ["intuit", "application", "software"]
    },
    "IT": {
        "name": "Gartner",
        "sector": "Information Technology",
        "industry": "IT Consulting & Other Services",
        "description": "Gartner - IT Consulting & Other Services",
        "keywords": ["gartner", "consulting", "other", "services"]
    },
    "JBL": {
        "name": "Jabil",
        "sector": "Information Technology",
        "industry": "Electronic Manufacturing Services",
        "description": "Jabil - Electronic Manufacturing Services",
        "keywords": ["jabil", "electronic", "manufacturing", "services"]
    },
    "KEYS": {
        "name": "Keysight Technologies",
        "sector": "Information Technology",
        "industry": "Electronic Equipment & Instruments",
        "description": "Keysight Technologies - Electronic Equipment & Instruments",
        "keywords": ["keysight", "technologies", "electronic", "equipment", "instruments"]
    },
    "MPWR": {
        "name": "Monolithic Power Systems",
        "sector": "Information Technology",
        "industry": "Semiconductors",
        "description": "Monolithic Power Systems - Semiconductors",
        "keywords": ["monolithic", "power", "systems", "semiconductors"]
    },
    "MSI": {
        "name": "Motorola Solutions",
        "sector": "Information Technology",
        "industry": "Communications Equipment",
        "description": "Motorola Solutions - Communications Equipment",
        "keywords": ["motorola", "solutions", "communications", "equipment"]
    },
    "NOW": {
        "name": "ServiceNow",
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "ServiceNow - Systems Software",
        "keywords": ["servicenow", "systems", "software"]
    },
    "NTAP": {
        "name": "NetApp",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "NetApp - Technology Hardware, Storage & Peripherals",
        "keywords": ["netapp", "technology", "hardware", "storage", "peripherals"]
    },
    "PANW": {
        "name": "Palo Alto Networks",
        "sector": "Information Technology",
        "industry": "Systems Software",
        "description": "Palo Alto Networks - Systems Software",
        "keywords": ["palo", "alto", "networks", "systems", "software"]
    },
    "PLTR": {
        "name": "Palantir Technologies",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Palantir Technologies - Application Software",
        "keywords": ["palantir", "technologies", "application", "software"]
    },
    "PTC": {
        "name": "PTC Inc.",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "PTC Inc. - Application Software",
        "keywords": ["ptc", "application", "software"]
    },
    "ROP": {
        "name": "Roper Technologies",
        "sector": "Information Technology",
        "industry": "Electronic Equipment & Instruments",
        "description": "Roper Technologies - Electronic Equipment & Instruments",
        "keywords": ["roper", "technologies", "electronic", "equipment", "instruments"]
    },
    "SMCI": {
        "name": "Supermicro",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Supermicro - Technology Hardware, Storage & Peripherals",
        "keywords": ["supermicro", "technology", "hardware", "storage", "peripherals"]
    },
    "SNPS": {
        "name": "Synopsys",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Synopsys - Application Software",
        "keywords": ["synopsys", "application", "software"]
    },
    "STX": {
        "name": "Seagate Technology",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Seagate Technology - Technology Hardware, Storage & Peripherals",
        "keywords": ["seagate", "technology", "hardware", "storage", "peripherals"]
    },
    "TDY": {
        "name": "Teledyne Technologies",
        "sector": "Information Technology",
        "industry": "Electronic Equipment & Instruments",
        "description": "Teledyne Technologies - Electronic Equipment & Instruments",
        "keywords": ["teledyne", "technologies", "electronic", "equipment", "instruments"]
    },
    "TEL": {
        "name": "TE Connectivity",
        "sector": "Information Technology",
        "industry": "Electronic Manufacturing Services",
        "description": "TE Connectivity - Electronic Manufacturing Services",
        "keywords": ["nnectivity", "electronic", "manufacturing", "services"]
    },
    "TER": {
        "name": "Teradyne",
        "sector": "Information Technology",
        "industry": "Semiconductor Materials & Equipment",
        "description": "Teradyne - Semiconductor Materials & Equipment",
        "keywords": ["teradyne", "semiconductor", "materials", "equipment"]
    },
    "TRMB": {
        "name": "Trimble Inc.",
        "sector": "Information Technology",
        "industry": "Electronic Equipment & Instruments",
        "description": "Trimble Inc. - Electronic Equipment & Instruments",
        "keywords": ["trimble", "electronic", "equipment", "instruments"]
    },
    "TYL": {
        "name": "Tyler Technologies",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Tyler Technologies - Application Software",
        "keywords": ["tyler", "technologies", "application", "software"]
    },
    "VRSN": {
        "name": "Verisign",
        "sector": "Information Technology",
        "industry": "Internet Services & Infrastructure",
        "description": "Verisign - Internet Services & Infrastructure",
        "keywords": ["verisign", "internet", "services", "infrastructure"]
    },
    "WDAY": {
        "name": "Workday, Inc.",
        "sector": "Information Technology",
        "industry": "Application Software",
        "description": "Workday, Inc. - Application Software",
        "keywords": ["workday", "application", "software"]
    },
    "WDC": {
        "name": "Western Digital",
        "sector": "Information Technology",
        "industry": "Technology Hardware, Storage & Peripherals",
        "description": "Western Digital - Technology Hardware, Storage & Peripherals",
        "keywords": ["western", "digital", "technology", "hardware", "storage", "peripherals"]
    },
    "ZBRA": {
        "name": "Zebra Technologies",
        "sector": "Information Technology",
        "industry": "Electronic Equipment & Instruments",
        "description": "Zebra Technologies - Electronic Equipment & Instruments",
        "keywords": ["zebra", "technologies", "electronic", "equipment", "instruments"]
    },

    # Communication Services (additional)
    "EA": {
        "name": "Electronic Arts",
        "sector": "Communication Services",
        "industry": "Interactive Home Entertainment",
        "description": "Electronic Arts - Interactive Home Entertainment",
        "keywords": ["electronic", "arts", "interactive", "home", "entertainment"]
    },
    "FOX": {
        "name": "Fox Corporation (Class B)",
        "sector": "Communication Services",
        "industry": "Broadcasting",
        "description": "Fox Corporation (Class B) - Broadcasting",
        "keywords": ["fox", "oration", "(class", "broadcasting"]
    },
    "FOXA": {
        "name": "Fox Corporation (Class A)",
        "sector": "Communication Services",
        "industry": "Broadcasting",
        "description": "Fox Corporation (Class A) - Broadcasting",
        "keywords": ["fox", "oration", "(class", "broadcasting"]
    },
    "IPG": {
        "name": "Interpublic Group of Companies (The)",
        "sector": "Communication Services",
        "industry": "Advertising",
        "description": "Interpublic Group of Companies (The) - Advertising",
        "keywords": ["interpublic", "group", "mpanies", "(the)", "advertising"]
    },
    "LYV": {
        "name": "Live Nation Entertainment",
        "sector": "Communication Services",
        "industry": "Movies & Entertainment",
        "description": "Live Nation Entertainment - Movies & Entertainment",
        "keywords": ["live", "nation", "entertainment", "movies"]
    },
    "MTCH": {
        "name": "Match Group",
        "sector": "Communication Services",
        "industry": "Interactive Media & Services",
        "description": "Match Group - Interactive Media & Services",
        "keywords": ["match", "group", "interactive", "media", "services"]
    },
    "NWS": {
        "name": "News Corp (Class B)",
        "sector": "Communication Services",
        "industry": "Publishing",
        "description": "News Corp (Class B) - Publishing",
        "keywords": ["news", "(class", "publishing"]
    },
    "NWSA": {
        "name": "News Corp (Class A)",
        "sector": "Communication Services",
        "industry": "Publishing",
        "description": "News Corp (Class A) - Publishing",
        "keywords": ["news", "(class", "publishing"]
    },
    "OMC": {
        "name": "Omnicom Group",
        "sector": "Communication Services",
        "industry": "Advertising",
        "description": "Omnicom Group - Advertising",
        "keywords": ["omnicom", "group", "advertising"]
    },
    "PSKY": {
        "name": "Paramount Skydance Corporation",
        "sector": "Communication Services",
        "industry": "Movies & Entertainment",
        "description": "Paramount Skydance Corporation - Movies & Entertainment",
        "keywords": ["paramount", "skydance", "oration", "movies", "entertainment"]
    },
    "TKO": {
        "name": "TKO Group Holdings",
        "sector": "Communication Services",
        "industry": "Movies & Entertainment",
        "description": "TKO Group Holdings - Movies & Entertainment",
        "keywords": ["tko", "group", "holdings", "movies", "entertainment"]
    },
    "TTD": {
        "name": "Trade Desk (The)",
        "sector": "Communication Services",
        "industry": "Advertising",
        "description": "Trade Desk (The) - Advertising",
        "keywords": ["trade", "desk", "(the)", "advertising"]
    },
    "TTWO": {
        "name": "Take-Two Interactive",
        "sector": "Communication Services",
        "industry": "Interactive Home Entertainment",
        "description": "Take-Two Interactive - Interactive Home Entertainment",
        "keywords": ["take-two", "interactive", "home", "entertainment"]
    },
    "WBD": {
        "name": "Warner Bros. Discovery",
        "sector": "Communication Services",
        "industry": "Broadcasting",
        "description": "Warner Bros. Discovery - Broadcasting",
        "keywords": ["warner", "bros", "discovery", "broadcasting"]
    },

    # Consumer Discretionary (additional)
    "ABNB": {
        "name": "Airbnb",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Airbnb - Hotels, Resorts & Cruise Lines",
        "keywords": ["airbnb", "hotels", "resorts", "cruise", "lines"]
    },
    "APTV": {
        "name": "Aptiv",
        "sector": "Consumer Discretionary",
        "industry": "Automotive Parts & Equipment",
        "description": "Aptiv - Automotive Parts & Equipment",
        "keywords": ["aptiv", "automotive", "parts", "equipment"]
    },
    "AZO": {
        "name": "AutoZone",
        "sector": "Consumer Discretionary",
        "industry": "Automotive Retail",
        "description": "AutoZone - Automotive Retail",
        "keywords": ["autozone", "automotive", "retail"]
    },
    "BBY": {
        "name": "Best Buy",
        "sector": "Consumer Discretionary",
        "industry": "Computer & Electronics Retail",
        "description": "Best Buy - Computer & Electronics Retail",
        "keywords": ["best", "buy", "computer", "electronics", "retail"]
    },
    "BKNG": {
        "name": "Booking Holdings",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Booking Holdings - Hotels, Resorts & Cruise Lines",
        "keywords": ["booking", "holdings", "hotels", "resorts", "cruise", "lines"]
    },
    "CCL": {
        "name": "Carnival",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Carnival - Hotels, Resorts & Cruise Lines",
        "keywords": ["carnival", "hotels", "resorts", "cruise", "lines"]
    },
    "CZR": {
        "name": "Caesars Entertainment",
        "sector": "Consumer Discretionary",
        "industry": "Casinos & Gaming",
        "description": "Caesars Entertainment - Casinos & Gaming",
        "keywords": ["caesars", "entertainment", "casinos", "gaming"]
    },
    "DASH": {
        "name": "DoorDash",
        "sector": "Consumer Discretionary",
        "industry": "Specialized Consumer Services",
        "description": "DoorDash - Specialized Consumer Services",
        "keywords": ["doordash", "specialized", "consumer", "services"]
    },
    "DECK": {
        "name": "Deckers Brands",
        "sector": "Consumer Discretionary",
        "industry": "Footwear",
        "description": "Deckers Brands - Footwear",
        "keywords": ["deckers", "brands", "footwear"]
    },
    "DHI": {
        "name": "D. R. Horton",
        "sector": "Consumer Discretionary",
        "industry": "Homebuilding",
        "description": "D. R. Horton - Homebuilding",
        "keywords": ["horton", "homebuilding"]
    },
    "DPZ": {
        "name": "Domino's",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Domino's - Restaurants",
        "keywords": ["domino's", "restaurants"]
    },
    "DRI": {
        "name": "Darden Restaurants",
        "sector": "Consumer Discretionary",
        "industry": "Restaurants",
        "description": "Darden Restaurants - Restaurants",
        "keywords": ["darden", "restaurants"]
    },
    "EBAY": {
        "name": "eBay Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Broadline Retail",
        "description": "eBay Inc. - Broadline Retail",
        "keywords": ["ebay", "broadline", "retail"]
    },
    "EXPE": {
        "name": "Expedia Group",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Expedia Group - Hotels, Resorts & Cruise Lines",
        "keywords": ["expedia", "group", "hotels", "resorts", "cruise", "lines"]
    },
    "GPC": {
        "name": "Genuine Parts Company",
        "sector": "Consumer Discretionary",
        "industry": "Distributors",
        "description": "Genuine Parts Company - Distributors",
        "keywords": ["genuine", "parts", "mpany", "distributors"]
    },
    "GRMN": {
        "name": "Garmin",
        "sector": "Consumer Discretionary",
        "industry": "Consumer Electronics",
        "description": "Garmin - Consumer Electronics",
        "keywords": ["garmin", "consumer", "electronics"]
    },
    "HAS": {
        "name": "Hasbro",
        "sector": "Consumer Discretionary",
        "industry": "Leisure Products",
        "description": "Hasbro - Leisure Products",
        "keywords": ["hasbro", "leisure", "products"]
    },
    "HLT": {
        "name": "Hilton Worldwide",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Hilton Worldwide - Hotels, Resorts & Cruise Lines",
        "keywords": ["hilton", "worldwide", "hotels", "resorts", "cruise", "lines"]
    },
    "KMX": {
        "name": "CarMax",
        "sector": "Consumer Discretionary",
        "industry": "Automotive Retail",
        "description": "CarMax - Automotive Retail",
        "keywords": ["carmax", "automotive", "retail"]
    },
    "LEN": {
        "name": "Lennar",
        "sector": "Consumer Discretionary",
        "industry": "Homebuilding",
        "description": "Lennar - Homebuilding",
        "keywords": ["lennar", "homebuilding"]
    },
    "LKQ": {
        "name": "LKQ Corporation",
        "sector": "Consumer Discretionary",
        "industry": "Distributors",
        "description": "LKQ Corporation - Distributors",
        "keywords": ["lkq", "oration", "distributors"]
    },
    "LULU": {
        "name": "Lululemon Athletica",
        "sector": "Consumer Discretionary",
        "industry": "Apparel, Accessories & Luxury Goods",
        "description": "Lululemon Athletica - Apparel, Accessories & Luxury Goods",
        "keywords": ["lululemon", "athletica", "apparel", "accessories", "luxury", "goods"]
    },
    "LVS": {
        "name": "Las Vegas Sands",
        "sector": "Consumer Discretionary",
        "industry": "Casinos & Gaming",
        "description": "Las Vegas Sands - Casinos & Gaming",
        "keywords": ["las", "vegas", "sands", "casinos", "gaming"]
    },
    "MAR": {
        "name": "Marriott International",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Marriott International - Hotels, Resorts & Cruise Lines",
        "keywords": ["marriott", "international", "hotels", "resorts", "cruise", "lines"]
    },
    "MGM": {
        "name": "MGM Resorts",
        "sector": "Consumer Discretionary",
        "industry": "Casinos & Gaming",
        "description": "MGM Resorts - Casinos & Gaming",
        "keywords": ["mgm", "resorts", "casinos", "gaming"]
    },
    "MHK": {
        "name": "Mohawk Industries",
        "sector": "Consumer Discretionary",
        "industry": "Home Furnishings",
        "description": "Mohawk Industries - Home Furnishings",
        "keywords": ["mohawk", "industries", "home", "furnishings"]
    },
    "NCLH": {
        "name": "Norwegian Cruise Line Holdings",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Norwegian Cruise Line Holdings - Hotels, Resorts & Cruise Lines",
        "keywords": ["norwegian", "cruise", "line", "holdings", "hotels", "resorts", "lines"]
    },
    "NKE": {
        "name": "Nike, Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Apparel, Accessories & Luxury Goods",
        "description": "Nike, Inc. - Apparel, Accessories & Luxury Goods",
        "keywords": ["nike", "apparel", "accessories", "luxury", "goods"]
    },
    "NVR": {
        "name": "NVR, Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Homebuilding",
        "description": "NVR, Inc. - Homebuilding",
        "keywords": ["nvr", "homebuilding"]
    },
    "ORLY": {
        "name": "O’Reilly Automotive",
        "sector": "Consumer Discretionary",
        "industry": "Automotive Retail",
        "description": "O’Reilly Automotive - Automotive Retail",
        "keywords": ["o\u2019reilly", "automotive", "retail"]
    },
    "PHM": {
        "name": "PulteGroup",
        "sector": "Consumer Discretionary",
        "industry": "Homebuilding",
        "description": "PulteGroup - Homebuilding",
        "keywords": ["pultegroup", "homebuilding"]
    },
    "POOL": {
        "name": "Pool Corporation",
        "sector": "Consumer Discretionary",
        "industry": "Distributors",
        "description": "Pool Corporation - Distributors",
        "keywords": ["pool", "oration", "distributors"]
    },
    "RCL": {
        "name": "Royal Caribbean Group",
        "sector": "Consumer Discretionary",
        "industry": "Hotels, Resorts & Cruise Lines",
        "description": "Royal Caribbean Group - Hotels, Resorts & Cruise Lines",
        "keywords": ["royal", "caribbean", "group", "hotels", "resorts", "cruise", "lines"]
    },
    "RL": {
        "name": "Ralph Lauren Corporation",
        "sector": "Consumer Discretionary",
        "industry": "Apparel, Accessories & Luxury Goods",
        "description": "Ralph Lauren Corporation - Apparel, Accessories & Luxury Goods",
        "keywords": ["ralph", "lauren", "oration", "apparel", "accessories", "luxury", "goods"]
    },
    "ROST": {
        "name": "Ross Stores",
        "sector": "Consumer Discretionary",
        "industry": "Apparel Retail",
        "description": "Ross Stores - Apparel Retail",
        "keywords": ["ross", "stores", "apparel", "retail"]
    },
    "TPR": {
        "name": "Tapestry, Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Apparel, Accessories & Luxury Goods",
        "description": "Tapestry, Inc. - Apparel, Accessories & Luxury Goods",
        "keywords": ["tapestry", "apparel", "accessories", "luxury", "goods"]
    },
    "TSCO": {
        "name": "Tractor Supply",
        "sector": "Consumer Discretionary",
        "industry": "Other Specialty Retail",
        "description": "Tractor Supply - Other Specialty Retail",
        "keywords": ["tractor", "supply", "other", "specialty", "retail"]
    },
    "ULTA": {
        "name": "Ulta Beauty",
        "sector": "Consumer Discretionary",
        "industry": "Other Specialty Retail",
        "description": "Ulta Beauty - Other Specialty Retail",
        "keywords": ["ulta", "beauty", "other", "specialty", "retail"]
    },
    "WSM": {
        "name": "Williams-Sonoma, Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Homefurnishing Retail",
        "description": "Williams-Sonoma, Inc. - Homefurnishing Retail",
        "keywords": ["williams-sonoma", "homefurnishing", "retail"]
    },
    "WYNN": {
        "name": "Wynn Resorts",
        "sector": "Consumer Discretionary",
        "industry": "Casinos & Gaming",
        "description": "Wynn Resorts - Casinos & Gaming",
        "keywords": ["wynn", "resorts", "casinos", "gaming"]
    },

    # Consumer Staples (additional)
    "ADM": {
        "name": "Archer Daniels Midland",
        "sector": "Consumer Staples",
        "industry": "Agricultural Products & Services",
        "description": "Archer Daniels Midland - Agricultural Products & Services",
        "keywords": ["archer", "daniels", "midland", "agricultural", "products", "services"]
    },
    "BF-B": {
        "name": "Brown–Forman",
        "sector": "Consumer Staples",
        "industry": "Distillers & Vintners",
        "description": "Brown–Forman - Distillers & Vintners",
        "keywords": ["brown\u2013forman", "distillers", "vintners"]
    },
    "BG": {
        "name": "Bunge Global",
        "sector": "Consumer Staples",
        "industry": "Agricultural Products & Services",
        "description": "Bunge Global - Agricultural Products & Services",
        "keywords": ["bunge", "global", "agricultural", "products", "services"]
    },
    "CAG": {
        "name": "Conagra Brands",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Conagra Brands - Packaged Foods & Meats",
        "keywords": ["nagra", "brands", "packaged", "foods", "meats"]
    },
    "CHD": {
        "name": "Church & Dwight",
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Church & Dwight - Household Products",
        "keywords": ["church", "dwight", "household", "products"]
    },
    "CLX": {
        "name": "Clorox",
        "sector": "Consumer Staples",
        "industry": "Household Products",
        "description": "Clorox - Household Products",
        "keywords": ["clorox", "household", "products"]
    },
    "CPB": {
        "name": "Campbell's Company (The)",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Campbell's Company (The) - Packaged Foods & Meats",
        "keywords": ["campbell's", "mpany", "(the)", "packaged", "foods", "meats"]
    },
    "DG": {
        "name": "Dollar General",
        "sector": "Consumer Staples",
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Dollar General - Consumer Staples Merchandise Retail",
        "keywords": ["dollar", "general", "consumer", "staples", "merchandise", "retail"]
    },
    "DLTR": {
        "name": "Dollar Tree",
        "sector": "Consumer Staples",
        "industry": "Consumer Staples Merchandise Retail",
        "description": "Dollar Tree - Consumer Staples Merchandise Retail",
        "keywords": ["dollar", "tree", "consumer", "staples", "merchandise", "retail"]
    },
    "EL": {
        "name": "Estée Lauder Companies (The)",
        "sector": "Consumer Staples",
        "industry": "Personal Care Products",
        "description": "Estée Lauder Companies (The) - Personal Care Products",
        "keywords": ["est\u00e9e", "lauder", "mpanies", "(the)", "personal", "care", "products"]
    },
    "GIS": {
        "name": "General Mills",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "General Mills - Packaged Foods & Meats",
        "keywords": ["general", "mills", "packaged", "foods", "meats"]
    },
    "HRL": {
        "name": "Hormel Foods",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Hormel Foods - Packaged Foods & Meats",
        "keywords": ["hormel", "foods", "packaged", "meats"]
    },
    "HSY": {
        "name": "Hershey Company (The)",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Hershey Company (The) - Packaged Foods & Meats",
        "keywords": ["hershey", "mpany", "(the)", "packaged", "foods", "meats"]
    },
    "K": {
        "name": "Kellanova",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Kellanova - Packaged Foods & Meats",
        "keywords": ["kellanova", "packaged", "foods", "meats"]
    },
    "KDP": {
        "name": "Keurig Dr Pepper",
        "sector": "Consumer Staples",
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Keurig Dr Pepper - Soft Drinks & Non-alcoholic Beverages",
        "keywords": ["keurig", "pepper", "soft", "drinks", "non-alcoholic", "beverages"]
    },
    "KHC": {
        "name": "Kraft Heinz",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Kraft Heinz - Packaged Foods & Meats",
        "keywords": ["kraft", "heinz", "packaged", "foods", "meats"]
    },
    "KR": {
        "name": "Kroger",
        "sector": "Consumer Staples",
        "industry": "Food Retail",
        "description": "Kroger - Food Retail",
        "keywords": ["kroger", "food", "retail"]
    },
    "KVUE": {
        "name": "Kenvue",
        "sector": "Consumer Staples",
        "industry": "Personal Care Products",
        "description": "Kenvue - Personal Care Products",
        "keywords": ["kenvue", "personal", "care", "products"]
    },
    "LW": {
        "name": "Lamb Weston",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Lamb Weston - Packaged Foods & Meats",
        "keywords": ["lamb", "weston", "packaged", "foods", "meats"]
    },
    "MDLZ": {
        "name": "Mondelez International",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Mondelez International - Packaged Foods & Meats",
        "keywords": ["mondelez", "international", "packaged", "foods", "meats"]
    },
    "MKC": {
        "name": "McCormick & Company",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "McCormick & Company - Packaged Foods & Meats",
        "keywords": ["mcrmick", "mpany", "packaged", "foods", "meats"]
    },
    "MNST": {
        "name": "Monster Beverage",
        "sector": "Consumer Staples",
        "industry": "Soft Drinks & Non-alcoholic Beverages",
        "description": "Monster Beverage - Soft Drinks & Non-alcoholic Beverages",
        "keywords": ["monster", "beverage", "soft", "drinks", "non-alcoholic", "beverages"]
    },
    "MO": {
        "name": "Altria",
        "sector": "Consumer Staples",
        "industry": "Tobacco",
        "description": "Altria - Tobacco",
        "keywords": ["altria", "tobacco"]
    },
    "PM": {
        "name": "Philip Morris International",
        "sector": "Consumer Staples",
        "industry": "Tobacco",
        "description": "Philip Morris International - Tobacco",
        "keywords": ["philip", "morris", "international", "tobacco"]
    },
    "SJM": {
        "name": "J.M. Smucker Company (The)",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "J.M. Smucker Company (The) - Packaged Foods & Meats",
        "keywords": ["smucker", "mpany", "(the)", "packaged", "foods", "meats"]
    },
    "STZ": {
        "name": "Constellation Brands",
        "sector": "Consumer Staples",
        "industry": "Distillers & Vintners",
        "description": "Constellation Brands - Distillers & Vintners",
        "keywords": ["nstellation", "brands", "distillers", "vintners"]
    },
    "SYY": {
        "name": "Sysco",
        "sector": "Consumer Staples",
        "industry": "Food Distributors",
        "description": "Sysco - Food Distributors",
        "keywords": ["sysco", "food", "distributors"]
    },
    "TAP": {
        "name": "Molson Coors Beverage Company",
        "sector": "Consumer Staples",
        "industry": "Brewers",
        "description": "Molson Coors Beverage Company - Brewers",
        "keywords": ["molson", "ors", "beverage", "mpany", "brewers"]
    },
    "TSN": {
        "name": "Tyson Foods",
        "sector": "Consumer Staples",
        "industry": "Packaged Foods & Meats",
        "description": "Tyson Foods - Packaged Foods & Meats",
        "keywords": ["tyson", "foods", "packaged", "meats"]
    },
    "WBA": {
        "name": "Walgreens Boots Alliance",
        "sector": "Consumer Staples",
        "industry": "Drug Retail",
        "description": "Walgreens Boots Alliance - Drug Retail",
        "keywords": ["walgreens", "boots", "alliance", "drug", "retail"]
    },

    # Health Care (additional)
    "A": {
        "name": "Agilent Technologies",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Agilent Technologies - Life Sciences Tools & Services",
        "keywords": ["agilent", "technologies", "life", "sciences", "tools", "services"]
    },
    "ALGN": {
        "name": "Align Technology",
        "sector": "Health Care",
        "industry": "Health Care Supplies",
        "description": "Align Technology - Health Care Supplies",
        "keywords": ["align", "technology", "health", "care", "supplies"]
    },
    "BAX": {
        "name": "Baxter International",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Baxter International - Health Care Equipment",
        "keywords": ["baxter", "international", "health", "care", "equipment"]
    },
    "BDX": {
        "name": "Becton Dickinson",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Becton Dickinson - Health Care Equipment",
        "keywords": ["becton", "dickinson", "health", "care", "equipment"]
    },
    "BSX": {
        "name": "Boston Scientific",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Boston Scientific - Health Care Equipment",
        "keywords": ["boston", "scientific", "health", "care", "equipment"]
    },
    "CAH": {
        "name": "Cardinal Health",
        "sector": "Health Care",
        "industry": "Health Care Distributors",
        "description": "Cardinal Health - Health Care Distributors",
        "keywords": ["cardinal", "health", "care", "distributors"]
    },
    "CI": {
        "name": "Cigna",
        "sector": "Health Care",
        "industry": "Health Care Services",
        "description": "Cigna - Health Care Services",
        "keywords": ["cigna", "health", "care", "services"]
    },
    "CNC": {
        "name": "Centene Corporation",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Centene Corporation - Managed Health Care",
        "keywords": ["centene", "oration", "managed", "health", "care"]
    },
    "COO": {
        "name": "Cooper Companies (The)",
        "sector": "Health Care",
        "industry": "Health Care Supplies",
        "description": "Cooper Companies (The) - Health Care Supplies",
        "keywords": ["oper", "mpanies", "(the)", "health", "care", "supplies"]
    },
    "COR": {
        "name": "Cencora",
        "sector": "Health Care",
        "industry": "Health Care Distributors",
        "description": "Cencora - Health Care Distributors",
        "keywords": ["cencora", "health", "care", "distributors"]
    },
    "CRL": {
        "name": "Charles River Laboratories",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Charles River Laboratories - Life Sciences Tools & Services",
        "keywords": ["charles", "river", "laboratories", "life", "sciences", "tools", "services"]
    },
    "CVS": {
        "name": "CVS Health",
        "sector": "Health Care",
        "industry": "Health Care Services",
        "description": "CVS Health - Health Care Services",
        "keywords": ["cvs", "health", "care", "services"]
    },
    "DGX": {
        "name": "Quest Diagnostics",
        "sector": "Health Care",
        "industry": "Health Care Services",
        "description": "Quest Diagnostics - Health Care Services",
        "keywords": ["quest", "diagnostics", "health", "care", "services"]
    },
    "DVA": {
        "name": "DaVita",
        "sector": "Health Care",
        "industry": "Health Care Services",
        "description": "DaVita - Health Care Services",
        "keywords": ["davita", "health", "care", "services"]
    },
    "DXCM": {
        "name": "Dexcom",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Dexcom - Health Care Equipment",
        "keywords": ["dexcom", "health", "care", "equipment"]
    },
    "ELV": {
        "name": "Elevance Health",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Elevance Health - Managed Health Care",
        "keywords": ["elevance", "health", "managed", "care"]
    },
    "EW": {
        "name": "Edwards Lifesciences",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Edwards Lifesciences - Health Care Equipment",
        "keywords": ["edwards", "lifesciences", "health", "care", "equipment"]
    },
    "GEHC": {
        "name": "GE HealthCare",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "GE HealthCare - Health Care Equipment",
        "keywords": ["healthcare", "health", "care", "equipment"]
    },
    "HCA": {
        "name": "HCA Healthcare",
        "sector": "Health Care",
        "industry": "Health Care Facilities",
        "description": "HCA Healthcare - Health Care Facilities",
        "keywords": ["hca", "healthcare", "health", "care", "facilities"]
    },
    "HOLX": {
        "name": "Hologic",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Hologic - Health Care Equipment",
        "keywords": ["hologic", "health", "care", "equipment"]
    },
    "HSIC": {
        "name": "Henry Schein",
        "sector": "Health Care",
        "industry": "Health Care Distributors",
        "description": "Henry Schein - Health Care Distributors",
        "keywords": ["henry", "schein", "health", "care", "distributors"]
    },
    "HUM": {
        "name": "Humana",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Humana - Managed Health Care",
        "keywords": ["humana", "managed", "health", "care"]
    },
    "IDXX": {
        "name": "Idexx Laboratories",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Idexx Laboratories - Health Care Equipment",
        "keywords": ["idexx", "laboratories", "health", "care", "equipment"]
    },
    "INCY": {
        "name": "Incyte",
        "sector": "Health Care",
        "industry": "Biotechnology",
        "description": "Incyte - Biotechnology",
        "keywords": ["yte", "biotechnology"]
    },
    "IQV": {
        "name": "IQVIA",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "IQVIA - Life Sciences Tools & Services",
        "keywords": ["iqvia", "life", "sciences", "tools", "services"]
    },
    "LH": {
        "name": "Labcorp",
        "sector": "Health Care",
        "industry": "Health Care Services",
        "description": "Labcorp - Health Care Services",
        "keywords": ["labcorp", "health", "care", "services"]
    },
    "MCK": {
        "name": "McKesson Corporation",
        "sector": "Health Care",
        "industry": "Health Care Distributors",
        "description": "McKesson Corporation - Health Care Distributors",
        "keywords": ["mckesson", "oration", "health", "care", "distributors"]
    },
    "MDT": {
        "name": "Medtronic",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Medtronic - Health Care Equipment",
        "keywords": ["medtronic", "health", "care", "equipment"]
    },
    "MOH": {
        "name": "Molina Healthcare",
        "sector": "Health Care",
        "industry": "Managed Health Care",
        "description": "Molina Healthcare - Managed Health Care",
        "keywords": ["molina", "healthcare", "managed", "health", "care"]
    },
    "MRK": {
        "name": "Merck & Co.",
        "sector": "Health Care",
        "industry": "Pharmaceuticals",
        "description": "Merck & Co. - Pharmaceuticals",
        "keywords": ["merck", "pharmaceuticals"]
    },
    "MTD": {
        "name": "Mettler Toledo",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Mettler Toledo - Life Sciences Tools & Services",
        "keywords": ["mettler", "toledo", "life", "sciences", "tools", "services"]
    },
    "PODD": {
        "name": "Insulet Corporation",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Insulet Corporation - Health Care Equipment",
        "keywords": ["insulet", "oration", "health", "care", "equipment"]
    },
    "RMD": {
        "name": "ResMed",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "ResMed - Health Care Equipment",
        "keywords": ["resmed", "health", "care", "equipment"]
    },
    "RVTY": {
        "name": "Revvity",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Revvity - Health Care Equipment",
        "keywords": ["revvity", "health", "care", "equipment"]
    },
    "SOLV": {
        "name": "Solventum",
        "sector": "Health Care",
        "industry": "Health Care Technology",
        "description": "Solventum - Health Care Technology",
        "keywords": ["solventum", "health", "care", "technology"]
    },
    "STE": {
        "name": "Steris",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Steris - Health Care Equipment",
        "keywords": ["steris", "health", "care", "equipment"]
    },
    "SYK": {
        "name": "Stryker Corporation",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Stryker Corporation - Health Care Equipment",
        "keywords": ["stryker", "oration", "health", "care", "equipment"]
    },
    "TECH": {
        "name": "Bio-Techne",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Bio-Techne - Life Sciences Tools & Services",
        "keywords": ["bio-techne", "life", "sciences", "tools", "services"]
    },
    "UHS": {
        "name": "Universal Health Services",
        "sector": "Health Care",
        "industry": "Health Care Facilities",
        "description": "Universal Health Services - Health Care Facilities",
        "keywords": ["universal", "health", "services", "care", "facilities"]
    },
    "VTRS": {
        "name": "Viatris",
        "sector": "Health Care",
        "industry": "Pharmaceuticals",
        "description": "Viatris - Pharmaceuticals",
        "keywords": ["viatris", "pharmaceuticals"]
    },
    "WAT": {
        "name": "Waters Corporation",
        "sector": "Health Care",
        "industry": "Life Sciences Tools & Services",
        "description": "Waters Corporation - Life Sciences Tools & Services",
        "keywords": ["waters", "oration", "life", "sciences", "tools", "services"]
    },
    "WST": {
        "name": "West Pharmaceutical Services",
        "sector": "Health Care",
        "industry": "Health Care Supplies",
        "description": "West Pharmaceutical Services - Health Care Supplies",
        "keywords": ["west", "pharmaceutical", "services", "health", "care", "supplies"]
    },
    "ZBH": {
        "name": "Zimmer Biomet",
        "sector": "Health Care",
        "industry": "Health Care Equipment",
        "description": "Zimmer Biomet - Health Care Equipment",
        "keywords": ["zimmer", "biomet", "health", "care", "equipment"]
    },
    "ZTS": {
        "name": "Zoetis",
        "sector": "Health Care",
        "industry": "Pharmaceuticals",
        "description": "Zoetis - Pharmaceuticals",
        "keywords": ["zoetis", "pharmaceuticals"]
    },

    # Financials (additional)
    "ACGL": {
        "name": "Arch Capital Group",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Arch Capital Group - Property & Casualty Insurance",
        "keywords": ["arch", "capital", "group", "property", "casualty", "insurance"]
    },
    "AIZ": {
        "name": "Assurant",
        "sector": "Financials",
        "industry": "Multi-line Insurance",
        "description": "Assurant - Multi-line Insurance",
        "keywords": ["assurant", "multi-line", "insurance"]
    },
    "AJG": {
        "name": "Arthur J. Gallagher & Co.",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Arthur J. Gallagher & Co. - Insurance Brokers",
        "keywords": ["arthur", "gallagher", "insurance", "brokers"]
    },
    "AMP": {
        "name": "Ameriprise Financial",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Ameriprise Financial - Asset Management & Custody Banks",
        "keywords": ["ameriprise", "financial", "asset", "management", "custody", "banks"]
    },
    "AON": {
        "name": "Aon plc",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Aon plc - Insurance Brokers",
        "keywords": ["aon", "plc", "insurance", "brokers"]
    },
    "APO": {
        "name": "Apollo Global Management",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Apollo Global Management - Asset Management & Custody Banks",
        "keywords": ["apollo", "global", "management", "asset", "custody", "banks"]
    },
    "BEN": {
        "name": "Franklin Resources",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Franklin Resources - Asset Management & Custody Banks",
        "keywords": ["franklin", "resources", "asset", "management", "custody", "banks"]
    },
    "BK": {
        "name": "BNY Mellon",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "BNY Mellon - Asset Management & Custody Banks",
        "keywords": ["bny", "mellon", "asset", "management", "custody", "banks"]
    },
    "BRK-B": {
        "name": "Berkshire Hathaway",
        "sector": "Financials",
        "industry": "Multi-Sector Holdings",
        "description": "Berkshire Hathaway - Multi-Sector Holdings",
        "keywords": ["berkshire", "hathaway", "multi-sector", "holdings"]
    },
    "BRO": {
        "name": "Brown & Brown",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Brown & Brown - Insurance Brokers",
        "keywords": ["brown", "insurance", "brokers"]
    },
    "BX": {
        "name": "Blackstone Inc.",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Blackstone Inc. - Asset Management & Custody Banks",
        "keywords": ["blackstone", "asset", "management", "custody", "banks"]
    },
    "CBOE": {
        "name": "Cboe Global Markets",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "Cboe Global Markets - Financial Exchanges & Data",
        "keywords": ["cboe", "global", "markets", "financial", "exchanges", "data"]
    },
    "CFG": {
        "name": "Citizens Financial Group",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Citizens Financial Group - Regional Banks",
        "keywords": ["citizens", "financial", "group", "regional", "banks"]
    },
    "CINF": {
        "name": "Cincinnati Financial",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Cincinnati Financial - Property & Casualty Insurance",
        "keywords": ["cincinnati", "financial", "property", "casualty", "insurance"]
    },
    "CME": {
        "name": "CME Group",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "CME Group - Financial Exchanges & Data",
        "keywords": ["cme", "group", "financial", "exchanges", "data"]
    },
    "COIN": {
        "name": "Coinbase",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "Coinbase - Financial Exchanges & Data",
        "keywords": ["inbase", "financial", "exchanges", "data"]
    },
    "CPAY": {
        "name": "Corpay",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Corpay - Transaction & Payment Processing Services",
        "keywords": ["transaction", "payment", "processing", "services"]
    },
    "EG": {
        "name": "Everest Group",
        "sector": "Financials",
        "industry": "Reinsurance",
        "description": "Everest Group - Reinsurance",
        "keywords": ["everest", "group", "reinsurance"]
    },
    "ERIE": {
        "name": "Erie Indemnity",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Erie Indemnity - Insurance Brokers",
        "keywords": ["erie", "indemnity", "insurance", "brokers"]
    },
    "FDS": {
        "name": "FactSet",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "FactSet - Financial Exchanges & Data",
        "keywords": ["factset", "financial", "exchanges", "data"]
    },
    "FI": {
        "name": "Fiserv",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Fiserv - Transaction & Payment Processing Services",
        "keywords": ["fiserv", "transaction", "payment", "processing", "services"]
    },
    "FIS": {
        "name": "Fidelity National Information Services",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Fidelity National Information Services - Transaction & Payment Processing Services",
        "keywords": ["fidelity", "national", "information", "services", "transaction", "payment", "processing"]
    },
    "FITB": {
        "name": "Fifth Third Bancorp",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Fifth Third Bancorp - Regional Banks",
        "keywords": ["fifth", "third", "bancorp", "regional", "banks"]
    },
    "GL": {
        "name": "Globe Life",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Globe Life - Life & Health Insurance",
        "keywords": ["globe", "life", "health", "insurance"]
    },
    "GPN": {
        "name": "Global Payments",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Global Payments - Transaction & Payment Processing Services",
        "keywords": ["global", "payments", "transaction", "payment", "processing", "services"]
    },
    "HBAN": {
        "name": "Huntington Bancshares",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Huntington Bancshares - Regional Banks",
        "keywords": ["huntington", "bancshares", "regional", "banks"]
    },
    "HIG": {
        "name": "Hartford (The)",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "Hartford (The) - Property & Casualty Insurance",
        "keywords": ["hartford", "(the)", "property", "casualty", "insurance"]
    },
    "ICE": {
        "name": "Intercontinental Exchange",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "Intercontinental Exchange - Financial Exchanges & Data",
        "keywords": ["intercontinental", "exchange", "financial", "exchanges", "data"]
    },
    "IVZ": {
        "name": "Invesco",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Invesco - Asset Management & Custody Banks",
        "keywords": ["invesco", "asset", "management", "custody", "banks"]
    },
    "JKHY": {
        "name": "Jack Henry & Associates",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Jack Henry & Associates - Transaction & Payment Processing Services",
        "keywords": ["jack", "henry", "associates", "transaction", "payment", "processing", "services"]
    },
    "KEY": {
        "name": "KeyCorp",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "KeyCorp - Regional Banks",
        "keywords": ["key", "regional", "banks"]
    },
    "KKR": {
        "name": "KKR & Co.",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "KKR & Co. - Asset Management & Custody Banks",
        "keywords": ["kkr", "asset", "management", "custody", "banks"]
    },
    "L": {
        "name": "Loews Corporation",
        "sector": "Financials",
        "industry": "Multi-line Insurance",
        "description": "Loews Corporation - Multi-line Insurance",
        "keywords": ["loews", "oration", "multi-line", "insurance"]
    },
    "MCO": {
        "name": "Moody's Corporation",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "Moody's Corporation - Financial Exchanges & Data",
        "keywords": ["moody's", "oration", "financial", "exchanges", "data"]
    },
    "MKTX": {
        "name": "MarketAxess",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "MarketAxess - Financial Exchanges & Data",
        "keywords": ["marketaxess", "financial", "exchanges", "data"]
    },
    "MMC": {
        "name": "Marsh McLennan",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Marsh McLennan - Insurance Brokers",
        "keywords": ["marsh", "mclennan", "insurance", "brokers"]
    },
    "MSCI": {
        "name": "MSCI Inc.",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "MSCI Inc. - Financial Exchanges & Data",
        "keywords": ["msci", "financial", "exchanges", "data"]
    },
    "MTB": {
        "name": "M&T Bank",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "M&T Bank - Regional Banks",
        "keywords": ["bank", "regional", "banks"]
    },
    "NDAQ": {
        "name": "Nasdaq, Inc.",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "Nasdaq, Inc. - Financial Exchanges & Data",
        "keywords": ["nasdaq", "financial", "exchanges", "data"]
    },
    "NTRS": {
        "name": "Northern Trust",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "Northern Trust - Asset Management & Custody Banks",
        "keywords": ["northern", "trust", "asset", "management", "custody", "banks"]
    },
    "PFG": {
        "name": "Principal Financial Group",
        "sector": "Financials",
        "industry": "Life & Health Insurance",
        "description": "Principal Financial Group - Life & Health Insurance",
        "keywords": ["principal", "financial", "group", "life", "health", "insurance"]
    },
    "RF": {
        "name": "Regions Financial Corporation",
        "sector": "Financials",
        "industry": "Regional Banks",
        "description": "Regions Financial Corporation - Regional Banks",
        "keywords": ["regions", "financial", "oration", "regional", "banks"]
    },
    "RJF": {
        "name": "Raymond James Financial",
        "sector": "Financials",
        "industry": "Investment Banking & Brokerage",
        "description": "Raymond James Financial - Investment Banking & Brokerage",
        "keywords": ["raymond", "james", "financial", "investment", "banking", "brokerage"]
    },
    "SPGI": {
        "name": "S&P Global",
        "sector": "Financials",
        "industry": "Financial Exchanges & Data",
        "description": "S&P Global - Financial Exchanges & Data",
        "keywords": ["global", "financial", "exchanges", "data"]
    },
    "STT": {
        "name": "State Street Corporation",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "State Street Corporation - Asset Management & Custody Banks",
        "keywords": ["state", "street", "oration", "asset", "management", "custody", "banks"]
    },
    "SYF": {
        "name": "Synchrony Financial",
        "sector": "Financials",
        "industry": "Consumer Finance",
        "description": "Synchrony Financial - Consumer Finance",
        "keywords": ["synchrony", "financial", "consumer", "finance"]
    },
    "TROW": {
        "name": "T. Rowe Price",
        "sector": "Financials",
        "industry": "Asset Management & Custody Banks",
        "description": "T. Rowe Price - Asset Management & Custody Banks",
        "keywords": ["rowe", "price", "asset", "management", "custody", "banks"]
    },
    "WRB": {
        "name": "W. R. Berkley Corporation",
        "sector": "Financials",
        "industry": "Property & Casualty Insurance",
        "description": "W. R. Berkley Corporation - Property & Casualty Insurance",
        "keywords": ["berkley", "oration", "property", "casualty", "insurance"]
    },
    "WTW": {
        "name": "Willis Towers Watson",
        "sector": "Financials",
        "industry": "Insurance Brokers",
        "description": "Willis Towers Watson - Insurance Brokers",
        "keywords": ["willis", "towers", "watson", "insurance", "brokers"]
    },
    "XYZ": {
        "name": "Block, Inc.",
        "sector": "Financials",
        "industry": "Transaction & Payment Processing Services",
        "description": "Block, Inc. - Transaction & Payment Processing Services",
        "keywords": ["block", "transaction", "payment", "processing", "services"]
    },

    # Industrials (additional)
    "ADP": {
        "name": "Automatic Data Processing",
        "sector": "Industrials",
        "industry": "Human Resource & Employment Services",
        "description": "Automatic Data Processing - Human Resource & Employment Services",
        "keywords": ["automatic", "data", "processing", "human", "resource", "employment", "services"]
    },
    "ALLE": {
        "name": "Allegion",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Allegion - Building Products",
        "keywords": ["allegion", "building", "products"]
    },
    "AME": {
        "name": "Ametek",
        "sector": "Industrials",
        "industry": "Electrical Components & Equipment",
        "description": "Ametek - Electrical Components & Equipment",
        "keywords": ["ametek", "electrical", "components", "equipment"]
    },
    "AOS": {
        "name": "A. O. Smith",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "A. O. Smith - Building Products",
        "keywords": ["smith", "building", "products"]
    },
    "AXON": {
        "name": "Axon Enterprise",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Axon Enterprise - Aerospace & Defense",
        "keywords": ["axon", "enterprise", "aerospace", "defense"]
    },
    "BLDR": {
        "name": "Builders FirstSource",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Builders FirstSource - Building Products",
        "keywords": ["builders", "firstsource", "building", "products"]
    },
    "BR": {
        "name": "Broadridge Financial Solutions",
        "sector": "Industrials",
        "industry": "Data Processing & Outsourced Services",
        "description": "Broadridge Financial Solutions - Data Processing & Outsourced Services",
        "keywords": ["broadridge", "financial", "solutions", "data", "processing", "outsourced", "services"]
    },
    "CARR": {
        "name": "Carrier Global",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Carrier Global - Building Products",
        "keywords": ["carrier", "global", "building", "products"]
    },
    "CHRW": {
        "name": "C.H. Robinson",
        "sector": "Industrials",
        "industry": "Air Freight & Logistics",
        "description": "C.H. Robinson - Air Freight & Logistics",
        "keywords": ["robinson", "air", "freight", "logistics"]
    },
    "CMI": {
        "name": "Cummins",
        "sector": "Industrials",
        "industry": "Construction Machinery & Heavy Transportation Equipment",
        "description": "Cummins - Construction Machinery & Heavy Transportation Equipment",
        "keywords": ["cummins", "construction", "machinery", "heavy", "transportation", "equipment"]
    },
    "CPRT": {
        "name": "Copart",
        "sector": "Industrials",
        "industry": "Diversified Support Services",
        "description": "Copart - Diversified Support Services",
        "keywords": ["part", "diversified", "support", "services"]
    },
    "CTAS": {
        "name": "Cintas",
        "sector": "Industrials",
        "industry": "Diversified Support Services",
        "description": "Cintas - Diversified Support Services",
        "keywords": ["cintas", "diversified", "support", "services"]
    },
    "DAL": {
        "name": "Delta Air Lines",
        "sector": "Industrials",
        "industry": "Passenger Airlines",
        "description": "Delta Air Lines - Passenger Airlines",
        "keywords": ["delta", "air", "lines", "passenger", "airlines"]
    },
    "DAY": {
        "name": "Dayforce",
        "sector": "Industrials",
        "industry": "Human Resource & Employment Services",
        "description": "Dayforce - Human Resource & Employment Services",
        "keywords": ["dayforce", "human", "resource", "employment", "services"]
    },
    "DE": {
        "name": "Deere & Company",
        "sector": "Industrials",
        "industry": "Agricultural & Farm Machinery",
        "description": "Deere & Company - Agricultural & Farm Machinery",
        "keywords": ["deere", "mpany", "agricultural", "farm", "machinery"]
    },
    "DOV": {
        "name": "Dover Corporation",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Dover Corporation - Industrial Machinery & Supplies & Components",
        "keywords": ["dover", "oration", "industrial", "machinery", "supplies", "components"]
    },
    "EFX": {
        "name": "Equifax",
        "sector": "Industrials",
        "industry": "Research & Consulting Services",
        "description": "Equifax - Research & Consulting Services",
        "keywords": ["equifax", "research", "consulting", "services"]
    },
    "EMR": {
        "name": "Emerson Electric",
        "sector": "Industrials",
        "industry": "Electrical Components & Equipment",
        "description": "Emerson Electric - Electrical Components & Equipment",
        "keywords": ["emerson", "electric", "electrical", "components", "equipment"]
    },
    "ETN": {
        "name": "Eaton Corporation",
        "sector": "Industrials",
        "industry": "Electrical Components & Equipment",
        "description": "Eaton Corporation - Electrical Components & Equipment",
        "keywords": ["eaton", "oration", "electrical", "components", "equipment"]
    },
    "EXPD": {
        "name": "Expeditors International",
        "sector": "Industrials",
        "industry": "Air Freight & Logistics",
        "description": "Expeditors International - Air Freight & Logistics",
        "keywords": ["expeditors", "international", "air", "freight", "logistics"]
    },
    "FAST": {
        "name": "Fastenal",
        "sector": "Industrials",
        "industry": "Trading Companies & Distributors",
        "description": "Fastenal - Trading Companies & Distributors",
        "keywords": ["fastenal", "trading", "companies", "distributors"]
    },
    "FDX": {
        "name": "FedEx",
        "sector": "Industrials",
        "industry": "Air Freight & Logistics",
        "description": "FedEx - Air Freight & Logistics",
        "keywords": ["fedex", "air", "freight", "logistics"]
    },
    "FTV": {
        "name": "Fortive",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Fortive - Industrial Machinery & Supplies & Components",
        "keywords": ["fortive", "industrial", "machinery", "supplies", "components"]
    },
    "GEV": {
        "name": "GE Vernova",
        "sector": "Industrials",
        "industry": "Heavy Electrical Equipment",
        "description": "GE Vernova - Heavy Electrical Equipment",
        "keywords": ["vernova", "heavy", "electrical", "equipment"]
    },
    "GNRC": {
        "name": "Generac",
        "sector": "Industrials",
        "industry": "Electrical Components & Equipment",
        "description": "Generac - Electrical Components & Equipment",
        "keywords": ["generac", "electrical", "components", "equipment"]
    },
    "GWW": {
        "name": "W. W. Grainger",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "W. W. Grainger - Industrial Machinery & Supplies & Components",
        "keywords": ["grainger", "industrial", "machinery", "supplies", "components"]
    },
    "HII": {
        "name": "Huntington Ingalls Industries",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Huntington Ingalls Industries - Aerospace & Defense",
        "keywords": ["huntington", "ingalls", "industries", "aerospace", "defense"]
    },
    "HON": {
        "name": "Honeywell",
        "sector": "Industrials",
        "industry": "Industrial Conglomerates",
        "description": "Honeywell - Industrial Conglomerates",
        "keywords": ["honeywell", "industrial", "conglomerates"]
    },
    "HUBB": {
        "name": "Hubbell Incorporated",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Hubbell Incorporated - Industrial Machinery & Supplies & Components",
        "keywords": ["hubbell", "orporated", "industrial", "machinery", "supplies", "components"]
    },
    "HWM": {
        "name": "Howmet Aerospace",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Howmet Aerospace - Aerospace & Defense",
        "keywords": ["howmet", "aerospace", "defense"]
    },
    "IEX": {
        "name": "IDEX Corporation",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "IDEX Corporation - Industrial Machinery & Supplies & Components",
        "keywords": ["idex", "oration", "industrial", "machinery", "supplies", "components"]
    },
    "IR": {
        "name": "Ingersoll Rand",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Ingersoll Rand - Industrial Machinery & Supplies & Components",
        "keywords": ["ingersoll", "rand", "industrial", "machinery", "supplies", "components"]
    },
    "ITW": {
        "name": "Illinois Tool Works",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Illinois Tool Works - Industrial Machinery & Supplies & Components",
        "keywords": ["illinois", "tool", "works", "industrial", "machinery", "supplies", "components"]
    },
    "J": {
        "name": "Jacobs Solutions",
        "sector": "Industrials",
        "industry": "Construction & Engineering",
        "description": "Jacobs Solutions - Construction & Engineering",
        "keywords": ["jacobs", "solutions", "construction", "engineering"]
    },
    "JBHT": {
        "name": "J.B. Hunt",
        "sector": "Industrials",
        "industry": "Cargo Ground Transportation",
        "description": "J.B. Hunt - Cargo Ground Transportation",
        "keywords": ["hunt", "cargo", "ground", "transportation"]
    },
    "JCI": {
        "name": "Johnson Controls",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Johnson Controls - Building Products",
        "keywords": ["johnson", "ntrols", "building", "products"]
    },
    "LDOS": {
        "name": "Leidos",
        "sector": "Industrials",
        "industry": "Diversified Support Services",
        "description": "Leidos - Diversified Support Services",
        "keywords": ["leidos", "diversified", "support", "services"]
    },
    "LHX": {
        "name": "L3Harris",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "L3Harris - Aerospace & Defense",
        "keywords": ["l3harris", "aerospace", "defense"]
    },
    "LII": {
        "name": "Lennox International",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Lennox International - Building Products",
        "keywords": ["lennox", "international", "building", "products"]
    },
    "LUV": {
        "name": "Southwest Airlines",
        "sector": "Industrials",
        "industry": "Passenger Airlines",
        "description": "Southwest Airlines - Passenger Airlines",
        "keywords": ["southwest", "airlines", "passenger"]
    },
    "MAS": {
        "name": "Masco",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Masco - Building Products",
        "keywords": ["masco", "building", "products"]
    },
    "MMM": {
        "name": "3M",
        "sector": "Industrials",
        "industry": "Industrial Conglomerates",
        "description": "3M - Industrial Conglomerates",
        "keywords": ["industrial", "conglomerates"]
    },
    "NDSN": {
        "name": "Nordson Corporation",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Nordson Corporation - Industrial Machinery & Supplies & Components",
        "keywords": ["nordson", "oration", "industrial", "machinery", "supplies", "components"]
    },
    "ODFL": {
        "name": "Old Dominion",
        "sector": "Industrials",
        "industry": "Cargo Ground Transportation",
        "description": "Old Dominion - Cargo Ground Transportation",
        "keywords": ["old", "dominion", "cargo", "ground", "transportation"]
    },
    "OTIS": {
        "name": "Otis Worldwide",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Otis Worldwide - Industrial Machinery & Supplies & Components",
        "keywords": ["otis", "worldwide", "industrial", "machinery", "supplies", "components"]
    },
    "PAYC": {
        "name": "Paycom",
        "sector": "Industrials",
        "industry": "Human Resource & Employment Services",
        "description": "Paycom - Human Resource & Employment Services",
        "keywords": ["paycom", "human", "resource", "employment", "services"]
    },
    "PAYX": {
        "name": "Paychex",
        "sector": "Industrials",
        "industry": "Human Resource & Employment Services",
        "description": "Paychex - Human Resource & Employment Services",
        "keywords": ["paychex", "human", "resource", "employment", "services"]
    },
    "PCAR": {
        "name": "Paccar",
        "sector": "Industrials",
        "industry": "Construction Machinery & Heavy Transportation Equipment",
        "description": "Paccar - Construction Machinery & Heavy Transportation Equipment",
        "keywords": ["paccar", "construction", "machinery", "heavy", "transportation", "equipment"]
    },
    "PH": {
        "name": "Parker Hannifin",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Parker Hannifin - Industrial Machinery & Supplies & Components",
        "keywords": ["parker", "hannifin", "industrial", "machinery", "supplies", "components"]
    },
    "PNR": {
        "name": "Pentair",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Pentair - Industrial Machinery & Supplies & Components",
        "keywords": ["pentair", "industrial", "machinery", "supplies", "components"]
    },
    "PWR": {
        "name": "Quanta Services",
        "sector": "Industrials",
        "industry": "Construction & Engineering",
        "description": "Quanta Services - Construction & Engineering",
        "keywords": ["quanta", "services", "construction", "engineering"]
    },
    "ROK": {
        "name": "Rockwell Automation",
        "sector": "Industrials",
        "industry": "Electrical Components & Equipment",
        "description": "Rockwell Automation - Electrical Components & Equipment",
        "keywords": ["rockwell", "automation", "electrical", "components", "equipment"]
    },
    "ROL": {
        "name": "Rollins, Inc.",
        "sector": "Industrials",
        "industry": "Environmental & Facilities Services",
        "description": "Rollins, Inc. - Environmental & Facilities Services",
        "keywords": ["rollins", "environmental", "facilities", "services"]
    },
    "RSG": {
        "name": "Republic Services",
        "sector": "Industrials",
        "industry": "Environmental & Facilities Services",
        "description": "Republic Services - Environmental & Facilities Services",
        "keywords": ["republic", "services", "environmental", "facilities"]
    },
    "SNA": {
        "name": "Snap-on",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Snap-on - Industrial Machinery & Supplies & Components",
        "keywords": ["snap-on", "industrial", "machinery", "supplies", "components"]
    },
    "SWK": {
        "name": "Stanley Black & Decker",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Stanley Black & Decker - Industrial Machinery & Supplies & Components",
        "keywords": ["stanley", "black", "decker", "industrial", "machinery", "supplies", "components"]
    },
    "TDG": {
        "name": "TransDigm Group",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "TransDigm Group - Aerospace & Defense",
        "keywords": ["transdigm", "group", "aerospace", "defense"]
    },
    "TT": {
        "name": "Trane Technologies",
        "sector": "Industrials",
        "industry": "Building Products",
        "description": "Trane Technologies - Building Products",
        "keywords": ["trane", "technologies", "building", "products"]
    },
    "TXT": {
        "name": "Textron",
        "sector": "Industrials",
        "industry": "Aerospace & Defense",
        "description": "Textron - Aerospace & Defense",
        "keywords": ["textron", "aerospace", "defense"]
    },
    "UAL": {
        "name": "United Airlines Holdings",
        "sector": "Industrials",
        "industry": "Passenger Airlines",
        "description": "United Airlines Holdings - Passenger Airlines",
        "keywords": ["united", "airlines", "holdings", "passenger"]
    },
    "UBER": {
        "name": "Uber",
        "sector": "Industrials",
        "industry": "Passenger Ground Transportation",
        "description": "Uber - Passenger Ground Transportation",
        "keywords": ["uber", "passenger", "ground", "transportation"]
    },
    "UPS": {
        "name": "United Parcel Service",
        "sector": "Industrials",
        "industry": "Air Freight & Logistics",
        "description": "United Parcel Service - Air Freight & Logistics",
        "keywords": ["united", "parcel", "service", "air", "freight", "logistics"]
    },
    "URI": {
        "name": "United Rentals",
        "sector": "Industrials",
        "industry": "Trading Companies & Distributors",
        "description": "United Rentals - Trading Companies & Distributors",
        "keywords": ["united", "rentals", "trading", "companies", "distributors"]
    },
    "VLTO": {
        "name": "Veralto",
        "sector": "Industrials",
        "industry": "Environmental & Facilities Services",
        "description": "Veralto - Environmental & Facilities Services",
        "keywords": ["veralto", "environmental", "facilities", "services"]
    },
    "VRSK": {
        "name": "Verisk Analytics",
        "sector": "Industrials",
        "industry": "Research & Consulting Services",
        "description": "Verisk Analytics - Research & Consulting Services",
        "keywords": ["verisk", "analytics", "research", "consulting", "services"]
    },
    "WAB": {
        "name": "Wabtec",
        "sector": "Industrials",
        "industry": "Construction Machinery & Heavy Transportation Equipment",
        "description": "Wabtec - Construction Machinery & Heavy Transportation Equipment",
        "keywords": ["wabtec", "construction", "machinery", "heavy", "transportation", "equipment"]
    },
    "WM": {
        "name": "Waste Management",
        "sector": "Industrials",
        "industry": "Environmental & Facilities Services",
        "description": "Waste Management - Environmental & Facilities Services",
        "keywords": ["waste", "management", "environmental", "facilities", "services"]
    },
    "XYL": {
        "name": "Xylem Inc.",
        "sector": "Industrials",
        "industry": "Industrial Machinery & Supplies & Components",
        "description": "Xylem Inc. - Industrial Machinery & Supplies & Components",
        "keywords": ["xylem", "industrial", "machinery", "supplies", "components"]
    },

    # Energy (additional)
    "APA": {
        "name": "APA Corporation",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "APA Corporation - Oil & Gas Exploration & Production",
        "keywords": ["apa", "oration", "oil", "gas", "exploration", "production"]
    },
    "CTRA": {
        "name": "Coterra",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Coterra - Oil & Gas Exploration & Production",
        "keywords": ["terra", "oil", "gas", "exploration", "production"]
    },
    "DVN": {
        "name": "Devon Energy",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Devon Energy - Oil & Gas Exploration & Production",
        "keywords": ["devon", "energy", "oil", "gas", "exploration", "production"]
    },
    "EQT": {
        "name": "EQT Corporation",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "EQT Corporation - Oil & Gas Exploration & Production",
        "keywords": ["eqt", "oration", "oil", "gas", "exploration", "production"]
    },
    "EXE": {
        "name": "Expand Energy",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Expand Energy - Oil & Gas Exploration & Production",
        "keywords": ["expand", "energy", "oil", "gas", "exploration", "production"]
    },
    "FANG": {
        "name": "Diamondback Energy",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Diamondback Energy - Oil & Gas Exploration & Production",
        "keywords": ["diamondback", "energy", "oil", "gas", "exploration", "production"]
    },
    "KMI": {
        "name": "Kinder Morgan",
        "sector": "Energy",
        "industry": "Oil & Gas Storage & Transportation",
        "description": "Kinder Morgan - Oil & Gas Storage & Transportation",
        "keywords": ["kinder", "morgan", "oil", "gas", "storage", "transportation"]
    },
    "MPC": {
        "name": "Marathon Petroleum",
        "sector": "Energy",
        "industry": "Oil & Gas Refining & Marketing",
        "description": "Marathon Petroleum - Oil & Gas Refining & Marketing",
        "keywords": ["marathon", "petroleum", "oil", "gas", "refining", "marketing"]
    },
    "OKE": {
        "name": "Oneok",
        "sector": "Energy",
        "industry": "Oil & Gas Storage & Transportation",
        "description": "Oneok - Oil & Gas Storage & Transportation",
        "keywords": ["oneok", "oil", "gas", "storage", "transportation"]
    },
    "OXY": {
        "name": "Occidental Petroleum",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Occidental Petroleum - Oil & Gas Exploration & Production",
        "keywords": ["occidental", "petroleum", "oil", "gas", "exploration", "production"]
    },
    "PSX": {
        "name": "Phillips 66",
        "sector": "Energy",
        "industry": "Oil & Gas Refining & Marketing",
        "description": "Phillips 66 - Oil & Gas Refining & Marketing",
        "keywords": ["phillips", "oil", "gas", "refining", "marketing"]
    },
    "TPL": {
        "name": "Texas Pacific Land Corporation",
        "sector": "Energy",
        "industry": "Oil & Gas Exploration & Production",
        "description": "Texas Pacific Land Corporation - Oil & Gas Exploration & Production",
        "keywords": ["texas", "pacific", "land", "oration", "oil", "gas", "exploration", "production"]
    },
    "TRGP": {
        "name": "Targa Resources",
        "sector": "Energy",
        "industry": "Oil & Gas Storage & Transportation",
        "description": "Targa Resources - Oil & Gas Storage & Transportation",
        "keywords": ["targa", "resources", "oil", "gas", "storage", "transportation"]
    },
    "VLO": {
        "name": "Valero Energy",
        "sector": "Energy",
        "industry": "Oil & Gas Refining & Marketing",
        "description": "Valero Energy - Oil & Gas Refining & Marketing",
        "keywords": ["valero", "energy", "oil", "gas", "refining", "marketing"]
    },
    "WMB": {
        "name": "Williams Companies",
        "sector": "Energy",
        "industry": "Oil & Gas Storage & Transportation",
        "description": "Williams Companies - Oil & Gas Storage & Transportation",
        "keywords": ["williams", "mpanies", "oil", "gas", "storage", "transportation"]
    },

    # Materials (additional)
    "ALB": {
        "name": "Albemarle Corporation",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "Albemarle Corporation - Specialty Chemicals",
        "keywords": ["albemarle", "oration", "specialty", "chemicals"]
    },
    "AMCR": {
        "name": "Amcor",
        "sector": "Materials",
        "industry": "Paper & Plastic Packaging Products & Materials",
        "description": "Amcor - Paper & Plastic Packaging Products & Materials",
        "keywords": ["amcor", "paper", "plastic", "packaging", "products", "materials"]
    },
    "AVY": {
        "name": "Avery Dennison",
        "sector": "Materials",
        "industry": "Paper & Plastic Packaging Products & Materials",
        "description": "Avery Dennison - Paper & Plastic Packaging Products & Materials",
        "keywords": ["avery", "dennison", "paper", "plastic", "packaging", "products", "materials"]
    },
    "BALL": {
        "name": "Ball Corporation",
        "sector": "Materials",
        "industry": "Metal, Glass & Plastic Containers",
        "description": "Ball Corporation - Metal, Glass & Plastic Containers",
        "keywords": ["ball", "oration", "metal", "glass", "plastic", "containers"]
    },
    "CF": {
        "name": "CF Industries",
        "sector": "Materials",
        "industry": "Fertilizers & Agricultural Chemicals",
        "description": "CF Industries - Fertilizers & Agricultural Chemicals",
        "keywords": ["industries", "fertilizers", "agricultural", "chemicals"]
    },
    "CTVA": {
        "name": "Corteva",
        "sector": "Materials",
        "industry": "Fertilizers & Agricultural Chemicals",
        "description": "Corteva - Fertilizers & Agricultural Chemicals",
        "keywords": ["rteva", "fertilizers", "agricultural", "chemicals"]
    },
    "EMN": {
        "name": "Eastman Chemical Company",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "Eastman Chemical Company - Specialty Chemicals",
        "keywords": ["eastman", "chemical", "mpany", "specialty", "chemicals"]
    },
    "FCX": {
        "name": "Freeport-McMoRan",
        "sector": "Materials",
        "industry": "Copper",
        "description": "Freeport-McMoRan - Copper",
        "keywords": ["freeport-mcmoran", "copper"]
    },
    "IFF": {
        "name": "International Flavors & Fragrances",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "International Flavors & Fragrances - Specialty Chemicals",
        "keywords": ["international", "flavors", "fragrances", "specialty", "chemicals"]
    },
    "IP": {
        "name": "International Paper",
        "sector": "Materials",
        "industry": "Paper & Plastic Packaging Products & Materials",
        "description": "International Paper - Paper & Plastic Packaging Products & Materials",
        "keywords": ["international", "paper", "plastic", "packaging", "products", "materials"]
    },
    "LYB": {
        "name": "LyondellBasell",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "LyondellBasell - Specialty Chemicals",
        "keywords": ["lyondellbasell", "specialty", "chemicals"]
    },
    "MLM": {
        "name": "Martin Marietta Materials",
        "sector": "Materials",
        "industry": "Construction Materials",
        "description": "Martin Marietta Materials - Construction Materials",
        "keywords": ["martin", "marietta", "materials", "construction"]
    },
    "MOS": {
        "name": "Mosaic Company (The)",
        "sector": "Materials",
        "industry": "Fertilizers & Agricultural Chemicals",
        "description": "Mosaic Company (The) - Fertilizers & Agricultural Chemicals",
        "keywords": ["mosaic", "mpany", "(the)", "fertilizers", "agricultural", "chemicals"]
    },
    "NEM": {
        "name": "Newmont",
        "sector": "Materials",
        "industry": "Gold",
        "description": "Newmont - Gold",
        "keywords": ["newmont", "gold"]
    },
    "NUE": {
        "name": "Nucor",
        "sector": "Materials",
        "industry": "Steel",
        "description": "Nucor - Steel",
        "keywords": ["nucor", "steel"]
    },
    "PKG": {
        "name": "Packaging Corporation of America",
        "sector": "Materials",
        "industry": "Paper & Plastic Packaging Products & Materials",
        "description": "Packaging Corporation of America - Paper & Plastic Packaging Products & Materials",
        "keywords": ["packaging", "oration", "america", "paper", "plastic", "products", "materials"]
    },
    "PPG": {
        "name": "PPG Industries",
        "sector": "Materials",
        "industry": "Specialty Chemicals",
        "description": "PPG Industries - Specialty Chemicals",
        "keywords": ["ppg", "industries", "specialty", "chemicals"]
    },
    "STLD": {
        "name": "Steel Dynamics",
        "sector": "Materials",
        "industry": "Steel",
        "description": "Steel Dynamics - Steel",
        "keywords": ["steel", "dynamics"]
    },
    "SW": {
        "name": "Smurfit Westrock",
        "sector": "Materials",
        "industry": "Paper & Plastic Packaging Products & Materials",
        "description": "Smurfit Westrock - Paper & Plastic Packaging Products & Materials",
        "keywords": ["smurfit", "westrock", "paper", "plastic", "packaging", "products", "materials"]
    },
    "VMC": {
        "name": "Vulcan Materials Company",
        "sector": "Materials",
        "industry": "Construction Materials",
        "description": "Vulcan Materials Company - Construction Materials",
        "keywords": ["vulcan", "materials", "mpany", "construction"]
    },

    # Real Estate (additional)
    "ARE": {
        "name": "Alexandria Real Estate Equities",
        "sector": "Real Estate",
        "industry": "Office REITs",
        "description": "Alexandria Real Estate Equities - Office REITs",
        "keywords": ["alexandria", "real", "estate", "equities", "office", "reits"]
    },
    "AVB": {
        "name": "AvalonBay Communities",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "AvalonBay Communities - Multi-Family Residential REITs",
        "keywords": ["avalonbay", "mmunities", "multi-family", "residential", "reits"]
    },
    "BXP": {
        "name": "BXP, Inc.",
        "sector": "Real Estate",
        "industry": "Office REITs",
        "description": "BXP, Inc. - Office REITs",
        "keywords": ["bxp", "office", "reits"]
    },
    "CBRE": {
        "name": "CBRE Group",
        "sector": "Real Estate",
        "industry": "Real Estate Services",
        "description": "CBRE Group - Real Estate Services",
        "keywords": ["cbre", "group", "real", "estate", "services"]
    },
    "CPT": {
        "name": "Camden Property Trust",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "Camden Property Trust - Multi-Family Residential REITs",
        "keywords": ["camden", "property", "trust", "multi-family", "residential", "reits"]
    },
    "CSGP": {
        "name": "CoStar Group",
        "sector": "Real Estate",
        "industry": "Real Estate Services",
        "description": "CoStar Group - Real Estate Services",
        "keywords": ["star", "group", "real", "estate", "services"]
    },
    "DOC": {
        "name": "Healthpeak Properties",
        "sector": "Real Estate",
        "industry": "Health Care REITs",
        "description": "Healthpeak Properties - Health Care REITs",
        "keywords": ["healthpeak", "properties", "health", "care", "reits"]
    },
    "EQR": {
        "name": "Equity Residential",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "Equity Residential - Multi-Family Residential REITs",
        "keywords": ["equity", "residential", "multi-family", "reits"]
    },
    "ESS": {
        "name": "Essex Property Trust",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "Essex Property Trust - Multi-Family Residential REITs",
        "keywords": ["essex", "property", "trust", "multi-family", "residential", "reits"]
    },
    "EXR": {
        "name": "Extra Space Storage",
        "sector": "Real Estate",
        "industry": "Self-Storage REITs",
        "description": "Extra Space Storage - Self-Storage REITs",
        "keywords": ["extra", "space", "storage", "self-storage", "reits"]
    },
    "FRT": {
        "name": "Federal Realty Investment Trust",
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Federal Realty Investment Trust - Retail REITs",
        "keywords": ["federal", "realty", "investment", "trust", "retail", "reits"]
    },
    "HST": {
        "name": "Host Hotels & Resorts",
        "sector": "Real Estate",
        "industry": "Hotel & Resort REITs",
        "description": "Host Hotels & Resorts - Hotel & Resort REITs",
        "keywords": ["host", "hotels", "resorts", "hotel", "resort", "reits"]
    },
    "INVH": {
        "name": "Invitation Homes",
        "sector": "Real Estate",
        "industry": "Single-Family Residential REITs",
        "description": "Invitation Homes - Single-Family Residential REITs",
        "keywords": ["invitation", "homes", "single-family", "residential", "reits"]
    },
    "IRM": {
        "name": "Iron Mountain",
        "sector": "Real Estate",
        "industry": "Other Specialized REITs",
        "description": "Iron Mountain - Other Specialized REITs",
        "keywords": ["iron", "mountain", "other", "specialized", "reits"]
    },
    "KIM": {
        "name": "Kimco Realty",
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Kimco Realty - Retail REITs",
        "keywords": ["kimco", "realty", "retail", "reits"]
    },
    "MAA": {
        "name": "Mid-America Apartment Communities",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "Mid-America Apartment Communities - Multi-Family Residential REITs",
        "keywords": ["mid-america", "apartment", "mmunities", "multi-family", "residential", "reits"]
    },
    "O": {
        "name": "Realty Income",
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Realty Income - Retail REITs",
        "keywords": ["realty", "ome", "retail", "reits"]
    },
    "PSA": {
        "name": "Public Storage",
        "sector": "Real Estate",
        "industry": "Self-Storage REITs",
        "description": "Public Storage - Self-Storage REITs",
        "keywords": ["public", "storage", "self-storage", "reits"]
    },
    "REG": {
        "name": "Regency Centers",
        "sector": "Real Estate",
        "industry": "Retail REITs",
        "description": "Regency Centers - Retail REITs",
        "keywords": ["regency", "centers", "retail", "reits"]
    },
    "SBAC": {
        "name": "SBA Communications",
        "sector": "Real Estate",
        "industry": "Telecom Tower REITs",
        "description": "SBA Communications - Telecom Tower REITs",
        "keywords": ["sba", "mmunications", "telecom", "tower", "reits"]
    },
    "UDR": {
        "name": "UDR, Inc.",
        "sector": "Real Estate",
        "industry": "Multi-Family Residential REITs",
        "description": "UDR, Inc. - Multi-Family Residential REITs",
        "keywords": ["udr", "multi-family", "residential", "reits"]
    },
    "VICI": {
        "name": "Vici Properties",
        "sector": "Real Estate",
        "industry": "Hotel & Resort REITs",
        "description": "Vici Properties - Hotel & Resort REITs",
        "keywords": ["vici", "properties", "hotel", "resort", "reits"]
    },
    "VTR": {
        "name": "Ventas",
        "sector": "Real Estate",
        "industry": "Health Care REITs",
        "description": "Ventas - Health Care REITs",
        "keywords": ["ventas", "health", "care", "reits"]
    },
    "WELL": {
        "name": "Welltower",
        "sector": "Real Estate",
        "industry": "Health Care REITs",
        "description": "Welltower - Health Care REITs",
        "keywords": ["welltower", "health", "care", "reits"]
    },
    "WY": {
        "name": "Weyerhaeuser",
        "sector": "Real Estate",
        "industry": "Timber REITs",
        "description": "Weyerhaeuser - Timber REITs",
        "keywords": ["weyerhaeuser", "timber", "reits"]
    },

    # Utilities (additional)
    "AEE": {
        "name": "Ameren",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Ameren - Multi-Utilities",
        "keywords": ["ameren", "multi-utilities"]
    },
    "AES": {
        "name": "AES Corporation",
        "sector": "Utilities",
        "industry": "Independent Power Producers & Energy Traders",
        "description": "AES Corporation - Independent Power Producers & Energy Traders",
        "keywords": ["aes", "oration", "independent", "power", "producers", "energy", "traders"]
    },
    "ATO": {
        "name": "Atmos Energy",
        "sector": "Utilities",
        "industry": "Gas Utilities",
        "description": "Atmos Energy - Gas Utilities",
        "keywords": ["atmos", "energy", "gas", "utilities"]
    },
    "AWK": {
        "name": "American Water Works",
        "sector": "Utilities",
        "industry": "Water Utilities",
        "description": "American Water Works - Water Utilities",
        "keywords": ["american", "water", "works", "utilities"]
    },
    "CEG": {
        "name": "Constellation Energy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Constellation Energy - Electric Utilities",
        "keywords": ["nstellation", "energy", "electric", "utilities"]
    },
    "CMS": {
        "name": "CMS Energy",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "CMS Energy - Multi-Utilities",
        "keywords": ["cms", "energy", "multi-utilities"]
    },
    "CNP": {
        "name": "CenterPoint Energy",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "CenterPoint Energy - Multi-Utilities",
        "keywords": ["centerpoint", "energy", "multi-utilities"]
    },
    "DTE": {
        "name": "DTE Energy",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "DTE Energy - Multi-Utilities",
        "keywords": ["dte", "energy", "multi-utilities"]
    },
    "ED": {
        "name": "Consolidated Edison",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Consolidated Edison - Multi-Utilities",
        "keywords": ["nsolidated", "edison", "multi-utilities"]
    },
    "EIX": {
        "name": "Edison International",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Edison International - Electric Utilities",
        "keywords": ["edison", "international", "electric", "utilities"]
    },
    "ES": {
        "name": "Eversource Energy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Eversource Energy - Electric Utilities",
        "keywords": ["eversource", "energy", "electric", "utilities"]
    },
    "ETR": {
        "name": "Entergy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Entergy - Electric Utilities",
        "keywords": ["entergy", "electric", "utilities"]
    },
    "EVRG": {
        "name": "Evergy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Evergy - Electric Utilities",
        "keywords": ["evergy", "electric", "utilities"]
    },
    "EXC": {
        "name": "Exelon",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Exelon - Electric Utilities",
        "keywords": ["exelon", "electric", "utilities"]
    },
    "FE": {
        "name": "FirstEnergy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "FirstEnergy - Electric Utilities",
        "keywords": ["firstenergy", "electric", "utilities"]
    },
    "LNT": {
        "name": "Alliant Energy",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Alliant Energy - Electric Utilities",
        "keywords": ["alliant", "energy", "electric", "utilities"]
    },
    "NI": {
        "name": "NiSource",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "NiSource - Multi-Utilities",
        "keywords": ["nisource", "multi-utilities"]
    },
    "NRG": {
        "name": "NRG Energy",
        "sector": "Utilities",
        "industry": "Independent Power Producers & Energy Traders",
        "description": "NRG Energy - Independent Power Producers & Energy Traders",
        "keywords": ["nrg", "energy", "independent", "power", "producers", "traders"]
    },
    "PCG": {
        "name": "PG&E Corporation",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "PG&E Corporation - Multi-Utilities",
        "keywords": ["pge", "oration", "multi-utilities"]
    },
    "PEG": {
        "name": "Public Service Enterprise Group",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Public Service Enterprise Group - Electric Utilities",
        "keywords": ["public", "service", "enterprise", "group", "electric", "utilities"]
    },
    "PNW": {
        "name": "Pinnacle West Capital",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Pinnacle West Capital - Multi-Utilities",
        "keywords": ["pinnacle", "west", "capital", "multi-utilities"]
    },
    "PPL": {
        "name": "PPL Corporation",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "PPL Corporation - Electric Utilities",
        "keywords": ["ppl", "oration", "electric", "utilities"]
    },
    "SRE": {
        "name": "Sempra",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Sempra - Multi-Utilities",
        "keywords": ["sempra", "multi-utilities"]
    },
    "VST": {
        "name": "Vistra Corp.",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "Vistra Corp. - Electric Utilities",
        "keywords": ["vistra", "electric", "utilities"]
    },
    "WEC": {
        "name": "WEC Energy Group",
        "sector": "Utilities",
        "industry": "Electric Utilities",
        "description": "WEC Energy Group - Electric Utilities",
        "keywords": ["wec", "energy", "group", "electric", "utilities"]
    },
    "XEL": {
        "name": "Xcel Energy",
        "sector": "Utilities",
        "industry": "Multi-Utilities",
        "description": "Xcel Energy - Multi-Utilities",
        "keywords": ["xcel", "energy", "multi-utilities"]
    },
}

# =============================================================================
# Auto-generated lookup dicts -- built from SP500_COMPANIES at import time
# so they always stay in sync when companies are added/removed.
# =============================================================================

# Organize by GICS sector
SECTORS: dict[str, list[str]] = {}
for _ticker, _info in SP500_COMPANIES.items():
    SECTORS.setdefault(_info["sector"], []).append(_ticker)

# Organize by GICS sub-industry
INDUSTRIES: dict[str, list[str]] = {}
for _ticker, _info in SP500_COMPANIES.items():
    INDUSTRIES.setdefault(_info["industry"], []).append(_ticker)

# Business categories for natural language matching
# These are curated aliases that map common search terms to tickers.
# The keyword search function handles the long tail; these handle the
# most common "give me X companies" queries.
BUSINESS_CATEGORIES = {
    "car manufacturers": ["TSLA", "F", "GM"],
    "car companies": ["TSLA", "F", "GM"],
    "automotive": ["TSLA", "F", "GM", "APTV"],
    "electric vehicle": ["TSLA"],
    "ev companies": ["TSLA"],
    "tech companies": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Information Technology"],
    "technology": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Information Technology"],
    "banks": [t for t, i in SP500_COMPANIES.items() if "bank" in i["industry"].lower()],
    "banking": [t for t, i in SP500_COMPANIES.items() if "bank" in i["industry"].lower()],
    "financial": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Financials"],
    "oil companies": [t for t, i in SP500_COMPANIES.items() if "oil" in i["industry"].lower() or "petroleum" in i["industry"].lower()],
    "energy companies": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Energy"],
    "pharmaceutical": [t for t, i in SP500_COMPANIES.items() if "pharma" in i["industry"].lower()],
    "drug companies": [t for t, i in SP500_COMPANIES.items() if "pharma" in i["industry"].lower() or "biotech" in i["industry"].lower()],
    "biotech": [t for t, i in SP500_COMPANIES.items() if "biotech" in i["industry"].lower()],
    "healthcare": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Health Care"],
    "retail": [t for t, i in SP500_COMPANIES.items() if "retail" in i["industry"].lower() or "store" in i["industry"].lower()],
    "retailers": [t for t, i in SP500_COMPANIES.items() if "retail" in i["industry"].lower() or "store" in i["industry"].lower()],
    "restaurant": [t for t, i in SP500_COMPANIES.items() if "restaurant" in i["industry"].lower()],
    "food": [t for t, i in SP500_COMPANIES.items() if "food" in i["industry"].lower() or "beverage" in i["industry"].lower()],
    "software": [t for t, i in SP500_COMPANIES.items() if "software" in i["industry"].lower()],
    "cloud": ["MSFT", "AMZN", "GOOGL", "GOOG", "ORCL", "CRM", "NOW", "WDAY"],
    "artificial intelligence": ["NVDA", "GOOGL", "GOOG", "MSFT", "META", "PLTR", "CRWD"],
    "ai": ["NVDA", "GOOGL", "GOOG", "MSFT", "META", "PLTR", "CRWD"],
    "social media": ["META", "GOOGL", "GOOG"],
    "semiconductors": [t for t, i in SP500_COMPANIES.items() if "semiconductor" in i["industry"].lower()],
    "chips": [t for t, i in SP500_COMPANIES.items() if "semiconductor" in i["industry"].lower()],
    "payment": [t for t, i in SP500_COMPANIES.items() if "payment" in i["industry"].lower() or "transaction" in i["industry"].lower()],
    "fintech": ["V", "MA", "PYPL", "FI", "GPN", "FIS"],
    "insurance": [t for t, i in SP500_COMPANIES.items() if "insurance" in i["industry"].lower()],
    "telecom": [t for t, i in SP500_COMPANIES.items() if "telecom" in i["industry"].lower() or "wireless" in i["industry"].lower()],
    "telecommunications": [t for t, i in SP500_COMPANIES.items() if "telecom" in i["industry"].lower() or "wireless" in i["industry"].lower()],
    "utilities": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Utilities"],
    "defense": [t for t, i in SP500_COMPANIES.items() if "defense" in i["industry"].lower() or "aerospace" in i["industry"].lower()],
    "aerospace": [t for t, i in SP500_COMPANIES.items() if "defense" in i["industry"].lower() or "aerospace" in i["industry"].lower()],
    "real estate": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Real Estate"],
    "entertainment": [t for t, i in SP500_COMPANIES.items() if "entertainment" in i["industry"].lower() or "movie" in i["industry"].lower()],
    "media": [t for t, i in SP500_COMPANIES.items() if "media" in i["industry"].lower() or "broadcast" in i["industry"].lower()],
    "streaming": ["NFLX", "DIS", "WBD"],
    "cybersecurity": ["CRWD", "PANW", "FTNT", "GEN"],
    "travel": ["BKNG", "EXPE", "MAR", "HLT", "CCL", "NCLH", "RCL", "UAL", "DAL", "LUV"],
    "hotels": ["MAR", "HLT"],
    "airlines": ["UAL", "DAL", "LUV"],
    "industrials": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Industrials"],
    "materials": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Materials"],
    "consumer staples": [t for t, i in SP500_COMPANIES.items() if i["sector"] == "Consumer Staples"],
}

def search_companies_by_keywords(keywords: list) -> list:
    """Search companies by keyword matching in business descriptions and keywords"""
    results = []
    keywords_lower = [k.lower() for k in keywords]
    
    for ticker, info in SP500_COMPANIES.items():
        # Check if any keyword matches company keywords, name, or description
        for keyword in keywords_lower:
            if (any(keyword in comp_keyword.lower() for comp_keyword in info["keywords"]) or
                keyword in info["name"].lower() or
                keyword in info["description"].lower() or
                keyword in info["sector"].lower() or
                keyword in info["industry"].lower()):
                results.append(ticker)
                break
    
    return list(set(results))

def search_companies_by_category(category: str) -> list:
    """Search companies by business category (e.g., 'car manufacturers', 'tech companies')"""
    category_lower = category.lower()
    if category_lower in BUSINESS_CATEGORIES:
        return BUSINESS_CATEGORIES[category_lower]
    
    # Fallback to keyword search
    return search_companies_by_keywords([category])

def get_companies_by_sector(sector: str) -> list:
    """Get all companies in a sector"""
    return SECTORS.get(sector, [])

def get_companies_by_industry(industry: str) -> list:
    """Get all companies in an industry"""
    return INDUSTRIES.get(industry, [])

def get_company_info(ticker: str) -> dict:
    """Get detailed information about a specific company"""
    return SP500_COMPANIES.get(ticker.upper(), {})

def find_similar_companies(ticker: str, max_results: int = 5) -> list:
    """Find companies similar to the given ticker based on sector and industry"""
    if ticker.upper() not in SP500_COMPANIES:
        return []
    
    company_info = SP500_COMPANIES[ticker.upper()]
    sector = company_info["sector"]
    industry = company_info["industry"]
    
    # Get companies in same industry first, then same sector
    similar = []
    
    # Same industry companies (excluding the input ticker)
    for tick, info in SP500_COMPANIES.items():
        if tick != ticker.upper() and info["industry"] == industry:
            similar.append(tick)
    
    # If not enough, add same sector companies
    if len(similar) < max_results:
        for tick, info in SP500_COMPANIES.items():
            if (tick != ticker.upper() and 
                tick not in similar and 
                info["sector"] == sector):
                similar.append(tick)
    
    return similar[:max_results]

# Financial criteria functions (placeholders for future enhancement)
def filter_by_market_cap(tickers: list, min_cap: float = None, max_cap: float = None) -> list:
    """Filter companies by market cap range (in billions)"""
    # This would require real-time market data integration
    # For now, return the input list unchanged
    return tickers

def filter_by_revenue_growth(tickers: list, min_growth: float = None) -> list:
    """Filter companies by revenue growth percentage"""
    # This would require financial data integration
    # For now, return the input list unchanged  
    return tickers

def filter_by_pe_ratio(tickers: list, min_pe: float = None, max_pe: float = None) -> list:
    """Filter companies by P/E ratio range"""
    # This would require financial data integration
    # For now, return the input list unchanged
    return tickers 