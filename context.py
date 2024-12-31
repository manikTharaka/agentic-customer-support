import PyPDF2


class PDFContextProvider:
    def __init__(self,fpath):
        self.fpath = fpath
        self.context_text = None
    
    def get_context(self):
        if self.context_text is None:
            self.context_text = self._read_pdf()

        return self.context_text

    def _read_pdf(self):
        with open(self.fpath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        return text
    

# product_details_context =""""
# Sleep Better Product Catalog
# 1. Ultra Comfort Mattress
# Price: $1,299 (Queen) Type: Hybrid (Memory Foam + Pocket Coils) Height: 12 inches
# Construction Layers:
# 2" Cooling Gel Memory Foam Top Layer
# 2" Responsive Comfort Foam
# 2" Transition Layer
# 6" Pocket Coil System (1,024 coils in Queen size)
# Key Features:
# Advanced temperature regulation with cooling gel technology
# Edge-to-edge support system
# Motion isolation technology
# Breathable quilted cover with silver-infused fibers
# CertiPUR-US® certified foams
# Compatible with adjustable bed bases
# Best For:
# Hot sleepers
# Couples
# Back and stomach sleepers
# Those needing extra edge support
# Available Sizes: Twin, Twin XL, Full, Queen, King, California King Warranty: 15 years Trial
# Period: 100 nights
# 2. Dream Sleep Mattress
# Price: $899 (Queen) Type: All-Foam Height: 10 inches
# Construction Layers:
# 2" Memory Foam Comfort Layer
# 2" Adaptive Support Foam
# 6" High-Density Base FoamKey Features:
# Pressure-relieving memory foam
# Open-cell foam technology for better airflow
# Removable and washable cover
# Zero motion transfer
# CertiPUR-US® certified foams
# Medium-firm feel (6/10 on firmness scale)
# Best For:
# Side sleepers
# Light to average weight sleepers
# Those seeking motion isolation
# Budget-conscious shoppers
# Available Sizes: Twin, Full, Queen, King Warranty: 10 years Trial Period: 100 nights
# 3. Luxury Cloud Mattress
# Price: $1,899 (Queen) Type: Hybrid (Latex + Memory Foam + Coils) Height: 14 inches
# Construction Layers:
# 2" Natural Latex Top Layer
# 2" Gel-Infused Memory Foam
# 2" Dynamic Response Foam
# 8" Zoned Support Coil System (1,744 coils in Queen size)
# Key Features:
# Organic cotton and wool cover
# Natural latex for durability and bounce
# Zoned lumbar support
# Enhanced edge support system
# Temperature neutral design
# Antimicrobial properties
# GOTS and GOLS certified materials
# Best For:
# Luxury seekers
# Those with back pain
# Combination sleepers
# Eco-conscious consumersAvailable Sizes: Twin XL, Full, Queen, King, California King, Split King Warranty: 25 years
# Trial Period: 180 nights
# 4. Essential Plus Mattress
# Price: $699 (Queen) Type: All-Foam Height: 8 inches
# Construction Layers:
# 1.5" Comfort Foam
# 2" Pressure Relief Foam
# 4.5" Support Core Foam
# Key Features:
# Budget-friendly option
# Medium-firm support
# Basic cooling properties
# Lightweight and easy to move
# CertiPUR-US® certified foams
# Ideal for guest rooms
# Best For:
# Guest rooms
# Children's rooms
# Temporary living situations
# Budget shoppers
# Available Sizes: Twin, Full, Queen Warranty: 5 years Trial Period: 60 nights
# 5. Performance Sport Mattress
# Price: $1,499 (Queen) Type: Hybrid (Performance Foam + Coils) Height: 13 inches
# Construction Layers:
# 2" Recovery Foam with Copper Infusion
# 2" High-Density Support Foam
# 2" Dynamic Response Layer
# 7" Reinforced Coil System (1,356 coils in Queen size)
# Key Features:
# Copper-infused foam for recovery
# Enhanced pressure point relief
# Specialized for athletic recovery
# Advanced cooling technology
# Antimicrobial properties
# Extra durability for active individuals
# Reinforced edge support
# Best For:
# Athletes and active individuals
# Those with active recovery needs
# Heavy sleepers
# Hot sleepers
# Available Sizes: Twin XL, Full, Queen, King, California King Warranty: 20 years Trial Period:
# 120 nights
# Common Features Across All Models
# Free delivery
# White glove delivery available (additional cost for some models)
# Made in USA
# Fire-resistant barrier (chemical-free)
# Compatible with most foundation types
# Rotating recommended (no flipping required)

# """