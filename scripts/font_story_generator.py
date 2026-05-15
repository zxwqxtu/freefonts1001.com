#!/usr/bin/env python3
"""
FreeFonts1001 每三天字体专题生成器
每隔3天生成 1 篇字体历史 / 设计师故事 / 趋势解读 专题页
文件名：[YYYY-MM-DD].html  →  保存在 /Users/a1/www/freefonts1001.com/
自动 git commit & push
"""

import os
import json
import re
import subprocess
import datetime
import random
import datetime
import re
from pathlib import Path

# ── 配置 ────────────────────────────────────────────────────────────
BASE_DIR  = Path("/Users/a1/www/freefonts1001.com")
SCRIPTS_DIR = BASE_DIR / "scripts"
SCRIPTS_DIR.mkdir(exist_ok=True)

GIT_NAME  = "FreeFonts1001 Bot"
GIT_EMAIL = "bot@freefonts1001.com"

# ── 专题主题库（轮换使用，保证每日新鲜感） ─────────────────────────────
TOPICS = [

    # ═══════════════════════════════════════════════════════════════════
    # A 类：字体历史（Font History）
    # ═══════════════════════════════════════════════════════════════════
    {
        "category": "Font History",
        "title": "The Unexpected Story of Helvetica — How a Font Became a Global Icon",
        "slug": "history-of-helvetica",
        "intro": "It's on the New York City subway, the American Airlines logo, and the tax forms of dozens of countries. Helvetica is arguably the most famous typeface in the world — and it almost didn't exist.",
        "sections": [
            {
                "heading": "Born in Switzerland, Not Germany",
                "body": "Helvetica was designed in 1957 by Max Miedinger with Alex Leuin in Münchenbuchsee, Switzerland — originally named 'Neue Haas Grotesk'. When Haas's German foundry released it internationally, they renamed it 'Helvetica' (Latin for 'Swiss') to sidestep anti-German sentiment in the post-war years. The name was a marketing decision, not a design one."
            },
            {
                "heading": "Why Designers Can't Stop Arguing About It",
                "body": "Helvetica is beloved and despised in equal measure. Its supporters praise its clarity, neutrality, and almost spiritual calm. Its critics call it 'the typeface of capitalism' — so neutral it has no soul. The documentary 'Helvetica' (2007) sparked a renewed global debate. Whatever your view, its influence on corporate branding and public signage is undeniable."
            },
            {
                "heading": "Where to See It Today",
                "body": "Scan your city: Helvetica is everywhere. The NYC MTA signs, the US IRS forms, the Lufthansa logo, Toyota's print ads, and countless government agencies worldwide use it. In 2022, Apple deprecated its system Helvetica font — a symbolic end of an era. Yet free alternatives like Arial (a Helvetica clone) ensure its visual DNA lives on in every browser."
            }
        ],
        "tags": ["history", "sans-serif", "classic", "branding"],
        "related_fonts": ["Helvetica", "Arial", "Inter", "Neue Haas Grotesk"],
        "read_time": "7 min read",
        "emoji": "🇨🇭"
    },

    {
        "category": "Font History",
        "title": "Garamond: The Font That Survived the Renaissance and Still Dominates Book Publishing",
        "slug": "history-of-garamond",
        "intro": "Claude Garamond cut his first punches in Paris around 1540. Nearly 500 years later, his letterforms still define what 'elegant book typography' looks like. How did one Renaissance punchcutter create something timeless?",
        "sections": [
            {
                "heading": "A Punchcutter Ahead of His Time",
                "body": "Claude Garamond was not just a craftsman — he was a typographic visionary. Working in Paris during the French Renaissance, he created typefaces with an unprecedented lightness and elegance. His early roman types were optically refined, with delicate hairline strokes and perfectly proportioned counters. His Greek types were so admired that they were used for scholarly printing for centuries. He essentially invented the concept of 'type design as fine art'."
            },
            {
                "heading": "Why Garamond Is the Gold Standard for Long-Form Reading",
                "body": "Print designers swear by Garamond for body text in books. The reasons are technical: moderate x-height, generous lowercase letters, open apertures, and careful ink trap design (small recesses at stroke intersections that prevent ink spread at small sizes). St. John's University Press, Penguin Classics, and most academic journals default to Garamond-based typesetting. Robert Slimbach's Adobe Garamond (1992) and Frank E. Blokland's Garamond Premier Pro are the modern standard-bearers."
            },
            {
                "heading": "The Garamond Revival Family",
                "body": "Today, over 40 digital Garamond revivals exist. The most notable: Adobe Garamond Pro (Slimbach, 1992), Garamond Premier Pro (Blokland, 2003 — most faithful to Garamond's originals), EB Garamond (Georg Mayr-Duffner, 2010 — free, open-source, variable), and Garamond Libre (Letraset, 1979 — widely distributed). Adobe Garamond Pro alone has 7 optical sizes, making it arguably the most scientifically precise revival ever made."
            }
        ],
        "tags": ["history", "serif", "books", "renaissance"],
        "related_fonts": ["Adobe Garamond", "EB Garamond", "Garamond Premier", "Cormorant"],
        "read_time": "6 min read",
        "emoji": "📖"
    },

    {
        "category": "Font History",
        "title": "Futura: The Bauhaus Font That Landed on the Moon",
        "slug": "history-of-futura",
        "intro": "In 1969, NASA used Futura for the lettering on the Apollo 11 lunar plaque. It was not a coincidence. Paul Renner's geometric sans-serif was designed to represent human progress, rationality, and the future — exactly the message NASA wanted to send.",
        "sections": [
            {
                "heading": "A Bauhaus Visionary, Banned by the Nazis",
                "body": "Paul Renner designed Futura in 1927 — 5 years before the Bauhaus school itself was closed by the Nazis. Futura was the Bauhaus ethos made type: geometric purity, functionalism, no ornament. Renner was arrested and briefly imprisoned by the Nazis in 1941 for his modernist views, despite Futura being his own design. His other works were confiscated. Yet the typeface survived and spread globally."
            },
            {
                "heading": "The Geometry Behind the Design",
                "body": "Futura's genius is mathematical. Every letterform is built on circles, triangles, and straight lines. The 'O' is a perfect circle. The 'A' is a triangle with a small cut. The strokes have uniform weight. This geometric construction creates an inherent sense of order and modernity. Yet Renner was careful: the forms are geometrically inspired, not slavishly constructed — he adjusted for optical corrections that make them feel right rather than mechanically rigid."
            },
            {
                "heading": "Cultural Ubiquity: From IKEA to Star Wars",
                "body": "Futura's cultural penetration is staggering. IKEA uses Futura LT (designed byaldó Frutiger, 1964). The original Star Wars title uses a Futura-based custom. Absolut Vodka's iconic label? Futura. The Volkswagen logo? Futura-adjacent. Gill Sans, itself a British response to Futura, dominates British publishing and the London Underground. Its geometry is so fundamental it became invisible — the mark of modernity itself."
            }
        ],
        "tags": ["history", "geometric", "bauhaus", "modernism"],
        "related_fonts": ["Futura", "Gill Sans", "Avenir", "Circular"],
        "read_time": "8 min read",
        "emoji": "🚀"
    },

    {
        "category": "Font History",
        "title": "Comic Sans: The Most Hated Font in History — And Why It's Misunderstood",
        "slug": "history-of-comic-sans",
        "intro": "In 1994, a Microsoft typographer named Vincent Connell created a font for a children's software program. He had no idea he was about to create the most polarizing typeface in history — one that would be banned from hospitals, reviled by designers, and defended with surprising passion by dyslexia researchers.",
        "sections": [
            {
                "heading": "The Accidental Infamy",
                "body": "Comic Sans was designed in 1994 for Microsoft Bob, a now-defunct software product meant to make Windows more approachable. The font was meant to feel like comic book lettering — casual, friendly, informal. When Windows 95 shipped, Microsoft used Comic Sans in the 'Help' interface. It spread. And spread. And spread. Soon it was appearing on funeral programs, medical prescriptions, government documents, and war memorials. The backlash was swift."
            },
            {
                "heading": "Why Dyslexia Researchers Actually Love It",
                "body": "Here's the twist: multiple studies suggest Comic Sans may actually be one of the better fonts for readers with dyslexia. The reasoning is technical: its distinct letter shapes (b vs d confusion is reduced by Comic Sans' quirky forms), informal spacing, and high x-height help some dyslexic readers. The UK's Royal National Institute of Blind People (RNIB) has used Comic Sans. The British Dyslexia Association recommends it. In 2014, the 'ban Comic Sans' movement met serious scientific pushback."
            },
            {
                "heading": "The Redesign That Redeemed It",
                "body": "In 2022, Microsoft designer Corey Holms created Comic Neue — a redesigned version that keeps Comic Sans' DNA while making it genuinely suitable for professional use. It became a minor internet sensation. Microsoft also released Comic Sans' official open-source version. Whatever your view, Comic Sans is a case study in how context determines whether typography works — and in the power of fonts to provoke genuine emotion."
            }
        ],
        "tags": ["history", "controversial", "accessibility", "comic"],
        "related_fonts": ["Comic Sans", "Comic Neue", "Chalkboard", "Peachy"],
        "read_time": "6 min read",
        "emoji": "😂"
    },

    {
        "category": "Font History",
        "title": "Bodoni: The Typeface That Defined Luxury — From Milan Fashion to Perfume Bottles",
        "slug": "history-of-bodoni",
        "intro": "Giambattista Bodoni was a printer, not just a type designer. His Manuale Tipografico (1818) is one of the most beautiful books ever printed — a celebration of typography as art. Bodoni's typeface defined the visual language of luxury two centuries before 'luxury branding' existed as a concept.",
        "sections": [
            {
                "heading": "The Printer Who Became a Type Designer",
                "body": "Bodoni (1740–1813) ran the Royal Printing House in Parma, Italy, appointed by the Duke of Parma. He became obsessed with the contrast between thick and thin strokes — pushing the extremes further than any designer before him. His typefaces feature razor-thin hairline serifs against enormous black strokes. It's dramatic, theatrical, and utterly unlike the subtle curves of Garamond or Caslon. Bodoni understood that typography could evoke emotion, not just transmit information."
            },
            {
                "heading": "The Anatomy of Luxury",
                "body": "What makes Bodoni 'luxury'? Three things: extreme stroke contrast (thick and thin in the same letter), perfectly geometric serifs (flat and razor-thin), and generous white space. Luxury brands use Bodoni because it signals precision, refinement, and exclusivity. Vogue, Harper's Bazaar, and dozens of perfume houses use Bodoni-based typefaces. The thin hairline strokes catch the light on glossy paper, creating a visual shimmer that cheaper printing cannot replicate."
            },
            {
                "heading": "Modern Bodoni Families",
                "body": "Bodoni has been revived by virtually every major type foundry. Today's versions: AM Bodoni (American Type Founders, 1909 — the classic American Bodoni), Bodoni Std (Adobe, 1995 — Adobe's revival), Bauer Bodoni (Linotype, 1927 — extremely high contrast), and Bodoni Moda (Michele Gex, 2019 — free on Google Fonts, the most accessible Bodoni today). Bodoni Moda is particularly notable for its variable font version — weight axis from Ultra Compressed to Ultra Bold."
            }
        ],
        "tags": ["history", "serif", "luxury", "editorial"],
        "related_fonts": ["Bodoni Moda", "Didot", "Roman", "AM Bodoni"],
        "read_time": "7 min read",
        "emoji": "✨"
    },

    # ═══════════════════════════════════════════════════════════════════
    # B 类：设计师故事（Designer Profiles）
    # ═══════════════════════════════════════════════════════════════════
    {
        "category": "Designer Profile",
        "title": "Jonathan Hoefler: The Type Designer Who Gave Typography Back Its Ambition",
        "slug": "jonathan-hoefler-profile",
        "intro": "Hoefler is the typographer behind the typefaces used in the Harry Potter books, Barack Obama's 2008 campaign, and the New York Times Magazine. He's also the founder of Hoefler&Co (formerly Hoefler Text), one of the most respected independent type foundries in the world.",
        "sections": [
            {
                "heading": "The Making of a Type Legend",
                "body": "Jonathan Hoefler grew up in a suburb of Chicago, studied at Yale's graphic design program, and got his first job at the New York Times. At the Times, he discovered that most of what was being called 'typography' was really just 'using default fonts.' He left in 1991 to start his own foundry with partner Tobias Frere-Jones, creating typefaces of unprecedented ambition. Their partnership lasted 20 years before a famous, acrimonious split that became a landmark case in intellectual property law for type designers."
            },
            {
                "heading": "Typography for the Masses: Gotham and Obama's 2008",
                "body": "Hoefler's Gotham became the defining typeface of Barack Obama's 2008 presidential campaign. The brief was simple: create a typeface that looked like it was found on a building in Chicago. The result — inspired by New Deal-era architectural lettering — became the most recognizable political brand asset in modern American history. Gotham was used on yard signs, websites, buses, and t-shirts. Hoefler famously offered it to the campaign for free, a decision that generated enormous goodwill and cemented his reputation as a designer with principles."
            },
            {
                "heading": "The Hoefler&Co Philosophy Today",
                "body": "Hoefler&Co now licenses over 1,200 typeface families and serves clients from Vogue to the US government. Their approach: obsessive optical refinement, deep historical research into letterform traditions, and a belief that type should communicate something genuinely new rather than merely serve as a vehicle for content. Their Discoverability project (2021) reimagined how type specimens work — presenting typefaces not as samples but as arguments about what typography can do."
            }
        ],
        "tags": ["designer", "foundry", "editorial", "american"],
        "related_fonts": ["Gotham", "Hoefler Text", "Mercury", "Tungsten"],
        "read_time": "8 min read",
        "emoji": "🗽"
    },

    {
        "category": "Designer Profile",
        "title": "Colophon Foundry: The Small London Studio Building Type for the World's Best Brands",
        "slug": "colophon-foundry-profile",
        "intro": "Founded in 2002 by Anthony Sheret and Edd Harrington in London, Colophon is one of the world's most respected independent type foundries. They don't chase trends — they create typefaces that are rigorously researched, beautifully made, and built to last decades.",
        "sections": [
            {
                "heading": "The Anti-Corporate Type Foundry",
                "body": "Colophon was born from frustration with the type industry. Sheret and Harrington, both trained designers, were exasperated by how difficult it was to use independent typefaces in real-world projects. Most foundries sold fonts at prices inaccessible to students and small studios. Colophon was built on a different principle: fair pricing, direct relationships with customers, and typefaces designed to work in the real world — not just in specimen books."
            },
            {
                "heading": "Apfel Groteesk and the Dutch Influence",
                "body": "Colophon's breakout hit was Apfel Groteesk (2014) — a grotesque sans-serif with a distinctly European character. The name translates roughly to 'Apple Big and Thick', a nod to the typography of German industrial catalogues from the 1930s. It became an instant classic, used by museums, publishers, and cultural institutions across Europe. The typeface has a quirky personality hidden beneath its apparently neutral surface — exactly the Colophon house style."
            },
            {
                "heading": "Why Independent Foundries Matter",
                "body": "In an era of consolidation (Adobe bought most major foundries in the 1990s-2000s), independent foundries like Colophon, Klim, Dinamo, and Occupant Fonts are where the most interesting type design happens. They're not trying to be everything to everyone. They're making typefaces for specific purposes, with specific philosophies, for designers who care deeply about what they're using. Colophon's library is intentionally small — each typeface takes years to develop."
            }
        ],
        "tags": ["designer", "foundry", "london", "independent"],
        "related_fonts": ["Apfel Groteesk", "General Sans", "Editorial New"],
        "read_time": "6 min read",
        "emoji": "🇬🇧"
    },

    {
        "category": "Designer Profile",
        "title": "Zuzana Licko: The Rebel Typographer Who Redefined What Screens Could Display",
        "slug": "zuzana-licko-profile",
        "intro": "Zuzana Licko co-founded Emigre — the magazine, the foundry, and the movement that changed how the world thinks about digital typography. In the mid-1980s, when most type was designed for print and screen rendering was primitive, Licko and her husband Rudy VanderLans created typefaces that embraced — rather than fought — the limitations of computer screens.",
        "sections": [
            {
                "heading": "Emigre: The Magazine That Started a Movement",
                "body": "In 1984, Zuzana Licko and Rudy VanderLans moved from Yugoslavia to California, carrying with them a passion for experimental typography and a Mac 512K. They started Emigre magazine — the first design journal to be designed on a computer, and one of the first to present typefaces as art rather than utility. Emigre became required reading for a generation of typographers who were discovering that the computer was not just a reproduction tool but a creative medium in its own right."
            },
            {
                "heading": "Designing for the Screen: The Resolution Independence Problem",
                "body": "Licko's genius was in embracing screen constraints rather than fighting them. Early computer screens had such low resolution (72-96 DPI) that traditional letterforms with fine details looked terrible. Licko designed typefaces specifically for these conditions — chunkier strokes, higher x-heights, more open apertures. Mrs Eaves (1996) is her masterpiece — a revival of Baskerville optimized for screen and digital contexts. It became the workhorse of digital editorial design for a decade."
            },
            {
                "heading": "Mrs Eaves: The Most Used Screen Serif of the Digital Era",
                "body": "Mrs Eaves is named after Sarah Eaves, the housekeeper and companion of John Baskerville (who was the subject of Licko's earlier typeface revival). The typeface combines the elegance of Baskerville with the digital functionality Licko pioneered. It's been used on hundreds of major editorial websites, including The New York Times' digital typography before their 2017 redesign. Licko continued to refine it across dozens of versions, each solving specific rendering problems on different platforms."
            }
        ],
        "tags": ["designer", "screen", "digital", "emigre"],
        "related_fonts": ["Mrs Eaves", "San Marco", "Temeraire", "Farao"],
        "read_time": "7 min read",
        "emoji": "💻"
    },

    {
        "category": "Designer Profile",
        "title": "Erik Spiekermann: The German Typographer Who Put Fonts on Motorways",
        "slug": "erik-spiekermann-profile",
        "intro": "Erik Spiekermann is the most influential living type designer in Germany — possibly the world. He's designed typefaces for motorway signage, Berlin's public transport, Deutsche Telekom, and a dozen major German corporations. He's also a publisher, professor, entrepreneur, and outspoken critic of bad typography.",
        "sections": [
            {
                "heading": "A Career Built on Public Typography",
                "body": "Spiekermann (born 1947) has spent his career designing typefaces for public use — the kind of typography millions of people encounter daily without thinking about it. His most famous work: the German motorway signage system, Berlin's BVG (public transport) typefaces, and the corporate identities of Deutsche Telekom and German television network ZDF. This public typography work is among the hardest in the field — it must be legible at speed, in all weather conditions, by people of all ages and reading abilities."
            },
            {
                "heading": "Meta, FF Meta, and the Corporate Type Revolution",
                "body": "FF Meta (1989–1991) was commissioned by German airline LTU as a corporate typeface, then released by FontFont. It was the typeface that introduced 'humanist sans-serif' thinking to European corporate design. Unlike the cold geometric sans-serifs of the 1970s-80s, Meta had warmth, optical corrections, and genuine readability. It became the standard for accessible, functional European design. Spiekermann's MetaDesign studio in Berlin, San Francisco, and New York became one of the most influential design consultancies of the 1990s."
            },
            {
                "heading": "The Open Source Pioneer: Spiekermann's Gift to the World",
                "body": "In 2014, Spiekermann released 13 of his typefaces under open-source licenses via the Spiekermann Design+Co website, with the support of Google. These included Spiekermann Sans (his corporate grotesque), Spiekermann Serif, and Vesterbro (a casual script). He argued that 'type should be free' — not as charity, but as a matter of principle. He also co-founded Fontstand, a font rental service that lets designers pay monthly for fonts rather than buying outright. Both moves reflected his belief that typography should be accessible to all designers, not just large corporations."
            }
        ],
        "tags": ["designer", "german", "public", "open-source"],
        "related_fonts": ["FF Meta", "Spiekermann Sans", "Spiekermann Serif", "Roboto"],
        "read_time": "8 min read",
        "emoji": "🇩🇪"
    },

    {
        "category": "Designer Profile",
        "title": "Jonathan Barnbrook: The Designer Behind the Most Iconic Album Covers of the 90s",
        "slug": "jonathan-barnbrook-profile",
        "intro": "Jonathan Barnbrook is a British type designer whose work for David Bowie's album 'Heathen' and 'Reality' — and more famously, Damien Hirst's graphic design and the film poster for 'The Usual Suspects' — made him the most recognizable living British typographer. His typefaces are used by artists, publishers, and brands who want typography with genuine personality.",
        "sections": [
            {
                "heading": "From Punk to Prestige",
                "body": "Barnbrook (born 1956) grew up in the British punk era — a background that deeply influenced his approach to typography. Where other type designers sought neutrality and invisibility, Barnbrook sought expression and edge. His early work combined commercial craft with artistic provocation. He studied at the Royal College of Art and founded his own studio in 1989. His first major typeface — a display face for an art exhibition — established his signature: type as emotional communication, not just functional vehicle."
            },
            {
                "heading": "Priori and the Virus Series",
                "body": "Priori (1994) is Barnbrook's most famous typeface — and one of the most widely used display typefaces of the 1990s. Its characteristic feature: irregular stroke widths that suggest hand-drawing while maintaining the structure of a refined serif. It's simultaneously elegant and imperfect. His 'Virus' typefaces (1995) took the opposite approach — deliberately distorted, corrupted, glitched letterforms that referenced digital decay. Both directions were influential: Priori spawned dozens of revivals; Virus became the visual vocabulary of 90s digital anxiety."
            },
            {
                "heading": "The Typography of David Bowie",
                "body": "Barnbrook's work for David Bowie spanned two decades and multiple iconic designs. The Heathen (2002) cover used a custom-modified version of his Sans typeface family — the redrawn letters creating an unsettling, otherworldly feeling perfectly suited to Bowie's final creative period. Barnbrook has said that the brief from Bowie was simply: 'Make it look like I'm still here.' The typography itself became a form of memorial. When Bowie died in 2016, Barnbrook's typefaces on those album covers became, for millions of fans, the visual language of grief."
            }
        ],
        "tags": ["designer", "british", "editorial", "art"],
        "related_fonts": ["Priori", "Sans", "News Gothic", "Lutherie"],
        "read_time": "7 min read",
        "emoji": "🎸"
    },

    # ═══════════════════════════════════════════════════════════════════
    # C 类：趋势解读（Trend Reports）
    # ═══════════════════════════════════════════════════════════════════
    {
        "category": "Trend Report",
        "title": "Variable Fonts in 2026: Why They're Finally Ready for Production",
        "slug": "variable-fonts-trend-2026",
        "intro": "Variable fonts were introduced in OpenType 1.8 in 2016. For years, they were hailed as the future of web typography — but browser support was uneven, tooling was immature, and the performance gains were hard to measure. In 2026, all that has changed. Variable fonts are now production-ready, and the case for adopting them has never been stronger.",
        "sections": [
            {
                "heading": "The Numbers: 60-80% File Size Reduction",
                "body": "A typical website loads 4-6 font weights (thin, light, regular, medium, bold, black) plus italics — totalling 600KB-2MB depending on the typeface. A variable font with a weight axis replaces all of those with a single file of 60-250KB. The CSS font-variation-settings property lets you set any weight from 100-900 with smooth interpolation. For a font like Inter, the variable version is 180KB vs. 1.2MB for the static weight set — an 85% reduction. At scale (millions of websites), this translates to terabytes of bandwidth saved daily."
            },
            {
                "heading": "What Axes Can Do: Beyond Weight",
                "body": "The weight axis (wght) is just the beginning. Modern variable fonts support: optical size (opsz) — automatically adjusts letterforms for screen vs. print sizes; width (wdth) — compresses or expands letterforms; slant (slnt) — italicizes without a separate file; and custom axes — designers can define any axis. Google Fonts now serves over 500 variable fonts. Figma, Adobe Illustrator, and all major browsers fully support variable fonts. The tooling problem is solved."
            },
            {
                "heading": "Real-World Performance Wins",
                "body": "Case study: GitHub switched to variable fonts and reduced their font payload by 40%. Instagram's redesign used variable fonts for their brand typeface (GT Walsheim). Shopify's Polaris design system now uses variable fonts exclusively. The performance benefits are real and measurable. In 2026, Google Fonts' variable font API allows you to subset and serve fonts with custom CSS axes on-the-fly — making variable fonts not just better, but simpler to implement than static font files."
            }
        ],
        "tags": ["trend", "variable-fonts", "performance", "web"],
        "related_fonts": ["Inter", "Roboto Flex", "Recursive", "Fraunces"],
        "read_time": "7 min read",
        "emoji": "📊"
    },

    {
        "category": "Trend Report",
        "title": "The AI Font Generation Landscape: What's Real, What's Hype in 2026",
        "slug": "ai-font-generation-trend-2026",
        "intro": "AI-generated typefaces have moved from novelty to genuine tools. In 2024, a typeface generated by AI won a prestigious typography award (causing immediate controversy). In 2026, major foundries are quietly integrating AI assistance into their workflows. This report separates the genuine capabilities from the hype.",
        "sections": [
            {
                "heading": "What AI Can Actually Do Today",
                "body": "Current AI font tools fall into three categories: (1) Style transfer — take a reference image or existing typeface, apply its style to new letterforms (Fontjoy, DeepFont); (2) Interpolation — generate intermediate weights and styles between existing typefaces; (3) Glyph completion — given a partial character set, AI completes the missing glyphs. The third category is genuinely useful: font designers spend 40% of their time on glyph completion. AI tools like Adobe's Generative Fill for fonts and Glyphs' AI assistant are now integrated into professional workflows."
            },
            {
                "heading": "What AI Cannot Do (Yet)",
                "body": "Genuinely new letterform design — the kind that requires understanding why certain forms work optically — is still beyond AI. Type designers create letterforms by understanding centuries of typographic tradition, optical illusion correction, and the specific communicative goals of a typeface. Current AI-generated typefaces lack the subtle optical corrections that separate professional work from amateur attempts. The award-winning AI typeface? Designers immediately pointed out that its 'flaws' — uneven stroke weights, inconsistent spacing — were obvious to trained eyes."
            },
            {
                "heading": "The Human-AI Collaboration Model",
                "body": "The productive use of AI in typography is as a productivity multiplier, not a replacement for human creativity. Fontifier generates decorative display typefaces from text prompts. Calligraphers use AI to analyze their own handwriting and generate complete script typefaces from samples. Design studios use AI to generate quick mockups to show clients before committing to months of manual design. FreeFonts1001's trend reports are AI-assisted. The winning model: AI handles the repetitive; humans handle the creative judgment. Neither can do the other's job."
            }
        ],
        "tags": ["trend", "ai", "future", "technology"],
        "related_fonts": ["AI-Generated", "GlyphNet", "Calligraphr"],
        "read_time": "8 min read",
        "emoji": "🤖"
    },

    {
        "category": "Trend Report",
        "title": "The Global Typography Renaissance: Non-Western Scripts Are Reshaping Digital Design",
        "slug": "non-western-typography-trend-2026",
        "intro": "For most of digital typography's history, Latin-script typefaces dominated. Japanese, Chinese, Arabic, and Devanagati typefaces were afterthoughts. In 2026, that era is over. The global internet means designers in Lagos, Seoul, Mumbai, and São Paulo are creating typefaces that bring non-Western typographic traditions into digital form — and Western designers are paying attention.",
        "sections": [
            {
                "heading": "Arabic Typography: From Calligraphy to Screen",
                "body": "Arabic script has been a center of typographic innovation for centuries — the Ottoman calligraphic tradition created sophisticated visual systems that had no Western equivalent. Digital Arabic typefaces historically suffered from poor rendering: diacritical marks disappeared, ligatures were broken, and text flow was unnatural. Google Fonts' Arabic initiative (launched 2017, expanded massively since) has created the first generation of digital Arabic typefaces designed from the ground up for screen. Noto Naskh Arabic, IBM Plex Arabic, and Tajawal represent genuine breakthroughs."
            },
            {
                "heading": "Chinese Type: The Challenge of 50,000 Characters",
                "body": "The challenge of Chinese typography is unique: a usable typeface requires at minimum 3,000-5,000 characters (GB2312), a comprehensive typeface 10,000+, and a truly complete typeface 50,000+ characters. This makes Chinese typeface design enormously expensive and slow. New AI-assisted glyph completion tools are changing this. Alibaba's PuHuiTi (2019) and Xiaomi's MiLanPro were among the first major Chinese variable fonts. The government-funded Chinese Typeface Open Source Project (2021) released 400+ open-source Chinese typefaces — a watershed moment for Chinese design culture."
            },
            {
                "heading": "Latin-Only Designers Are Catching Up",
                "body": "Western designers are increasingly incorporating non-Western typographic principles. Japanese typography's concept of ma (negative space) is influencing minimalist Western design. Korean Hangul's geometric logic is appearing in tech brand identities. Afrocentric type design (designers like Tré Seals of Vocal Type) is bringing Black American typography traditions into the digital era. The result: a genuinely global typography culture where no single tradition dominates, and the best ideas cross-pollinate across scripts."
            }
        ],
        "tags": ["trend", "global", "non-western", "cultural"],
        "related_fonts": ["Noto", "PuHuiTi", "IBM Plex", "Recoleta"],
        "read_time": "7 min read",
        "emoji": "🌍"
    },

    {
        "category": "Trend Report",
        "title": "Dark Mode Typography: The Hidden Challenges of Inverting Your Design System",
        "slug": "dark-mode-typography-trend-2026",
        "intro": "Apple made dark mode mainstream in 2019. By 2026, virtually every major app and website offers a dark option. But most design systems were built for light backgrounds — and typography doesn't simply 'invert.' Dark mode introduces genuine typographic challenges that most designers are still figuring out.",
        "sections": [
            {
                "heading": "Why Dark Mode Typography Is Harder Than It Looks",
                "body": "On light backgrounds, black text with moderate gray tones is easy to read. On dark backgrounds, pure white text creates halation — the bright text blooms into the surrounding dark space, reducing legibility. The fix isn't simply 'use off-white.' It requires understanding how human vision perceives light vs. dark differently. Research shows that on dark backgrounds, a font color of approximately #E0E0E0 (not pure white) combined with slightly increased letter-spacing and line-height performs significantly better than pure white at 16px."
            },
            {
                "heading": "Typeface Families Built for Both Modes",
                "body": "Not all typefaces work equally well in dark mode. Sans-serifs with high x-heights and open apertures (Inter, SF Pro, Manrope) perform best. High-contrast serifs with fine hairline strokes (Bodoni, Didot) look stunning in light mode but suffer in dark mode — the thin strokes become difficult to read against dark backgrounds. New 'dark-first' typefaces are emerging: designed specifically for dark backgrounds with thicker strokes, higher contrast, and optical adjustments that compensate for dark-mode halation. These include Manrope, Outfit, Satoshi, and Figtree."
            },
            {
                "heading": "CSS Variable Typography: The Modern Solution",
                "body": "Modern CSS makes dark-mode typography manageable through custom properties. Define your font colors, sizes, weights, and letter-spacing as CSS variables that switch based on the color scheme. The most sophisticated design systems (like IBM's Carbon) use 20+ typographic variables for dark mode — not just color, but adjusted letter-spacing, line-height, and even weight. Variable fonts make this even easier: you can adjust the weight axis to compensate for the perception difference between light and dark modes without loading separate font files."
            }
        ],
        "tags": ["trend", "dark-mode", "web-design", "ux"],
        "related_fonts": ["Inter", "Manrope", "Satoshi", "Figtree"],
        "read_time": "6 min read",
        "emoji": "🌙"
    },

    {
        "category": "Trend Report",
        "title": "Mono Fonts Are Having a Moment: From Code Editors to Fashion Magazines",
        "slug": "monospace-typography-trend-2026",
        "intro": "Monospace fonts spent decades in a single niche: code editors and terminal windows. In 2026, they've escaped. JetBrains Mono is a top-10 most downloaded font on Google Fonts. Monospace typefaces are appearing in fashion editorial, luxury branding, and consumer product design. Here's why — and what it means.",
        "sections": [
            {
                "heading": "Why Now: The Code Culture Explosion",
                "body": "Coding went mainstream in the 2010s. GitHub, Stack Overflow, and Hacker News created a culture where monospace text was visible to millions of non-programmers. 'Developer aesthetics' — which includes monospace typefaces — became cool through the influence of tech companies, startup culture, and the broader 'maker' movement. When Stripe's branding used a monospace typeface for its developer documentation, it signaled that monospace was no longer just functional — it was aspirational."
            },
            {
                "heading": "Fashion's Monospace Moment",
                "body": "The fashion industry's adoption of monospace type is deliberate and meaningful. Vetements' 2016 runway show used Courier (the typewriter typeface) for its logo — deliberately low-tech, anti-aspirational, working-class. Since then, monospace fonts have appeared in Balenciaga campaigns, Off-White marketing materials, and high-end magazine layouts. The paradox: a typeface born from the mechanical constraints of typewriters has become a symbol of authenticity, anti-establishment cool, and irony. Its very limitation — fixed character width — is perceived as honesty."
            },
            {
                "heading": "The New Monospace: JetBrains Mono, Fira Code, and Iosevka",
                "body": "Three typefaces dominate the modern code editor market. JetBrains Mono (2020) — the most popular new monospace font, designed specifically for developers with improved legibility and ligatures. Fira Code (2017) — Mozilla's contribution, famous for its programming ligatures (→, <=, != rendered as single symbols). Iosevka (2015, continuously updated) — the most customizable monospace typeface in existence, with thousands of build-time options. All three are open-source. JetBrains Mono alone has been downloaded over 10 million times from Google Fonts."
            }
        ],
        "tags": ["trend", "monospace", "code", "fashion"],
        "related_fonts": ["JetBrains Mono", "Fira Code", "Iosevka", "Courier"],
        "read_time": "6 min read",
        "emoji": "⌨️"
    },
]


# ── HTML 模板 ────────────────────────────────────────────────────────────
STORY_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | FreeFonts1001 Daily Story</title>
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{meta_keywords}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="article">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f0f0f; --surface: #1a1a1a; --surface2: #252525;
            --accent: #e8c547; --accent2: #ff6b35; --text: #f0ece3;
            --text-dim: #9b9589; --border: #2e2e2e;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; line-height: 1.75; }}
        a {{ color: var(--accent); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        /* ── Header ── */
        .site-header {{
            border-bottom: 1px solid var(--border);
            padding: 16px 40px;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .site-logo {{
            font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700;
            color: var(--text); text-decoration: none;
        }}
        .site-logo em {{ color: var(--accent); font-style: italic; }}
        .site-nav {{ font-size: 13px; color: var(--text-dim); }}
        .site-nav a {{ color: var(--text-dim); margin-left: 24px; }}
        .site-nav a:hover {{ color: var(--accent); }}

        /* ── Hero ── */
        .article-hero {{
            padding: 80px 40px 60px;
            max-width: 860px; margin: 0 auto;
        }}
        .article-meta {{
            display: flex; align-items: center; gap: 16px;
            font-size: 12px; color: var(--text-dim);
            letter-spacing: 1px; text-transform: uppercase; margin-bottom: 24px;
        }}
        .article-category {{
            background: rgba(232,197,71,0.12); color: var(--accent);
            border: 1px solid rgba(232,197,71,0.25); padding: 3px 12px;
            border-radius: 20px; font-weight: 600;
        }}
        .article-emoji {{ font-size: 48px; margin-bottom: 20px; }}
        h1 {{
            font-family: 'Playfair Display', serif; font-size: clamp(32px, 5vw, 58px);
            font-weight: 700; line-height: 1.1; margin-bottom: 24px;
            letter-spacing: -1px;
        }}
        .article-intro {{
            font-size: 18px; color: var(--text-dim); font-weight: 300;
            max-width: 680px; border-left: 3px solid var(--accent);
            padding-left: 20px; margin-bottom: 16px;
        }}
        .article-info {{ font-size: 13px; color: var(--text-dim); margin-top: 8px; }}

        /* ── Content ── */
        .article-body {{ max-width: 740px; margin: 0 auto; padding: 0 40px 80px; }}
        .article-content {{}}
        .article-section {{
            margin-bottom: 52px; padding-bottom: 52px;
            border-bottom: 1px solid var(--border);
        }}
        .article-section:last-child {{ border-bottom: none; }}
        .article-section h2 {{
            font-family: 'Playfair Display', serif; font-size: 26px;
            font-weight: 700; margin-bottom: 18px; line-height: 1.2;
        }}
        .article-section h2::before {{
            content: '{section_marker} '; color: var(--accent); margin-right: 8px;
        }}
        .article-section p {{ font-size: 16px; color: var(--text-dim); margin-bottom: 16px; }}
        .article-section p:last-child {{ margin-bottom: 0; }}

        /* ── Related Fonts ── */
        .related-fonts {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 16px; padding: 32px; margin: 52px 0;
        }}
        .related-fonts h3 {{
            font-size: 13px; letter-spacing: 2px; text-transform: uppercase;
            color: var(--accent); margin-bottom: 16px;
        }}
        .font-chips {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .font-chip {{
            background: var(--surface2); border: 1px solid var(--border);
            padding: 8px 16px; border-radius: 8px; font-size: 14px;
            font-weight: 600; color: var(--text); cursor: pointer;
            transition: all 0.2s;
        }}
        .font-chip:hover {{ border-color: var(--accent); color: var(--accent); transform: translateY(-1px); }}

        /* ── Tags ── */
        .article-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 32px 0; }}
        .tag {{
            font-size: 11px; background: var(--surface); color: var(--text-dim);
            border: 1px solid var(--border); padding: 4px 12px; border-radius: 20px;
            text-transform: uppercase; letter-spacing: 1px;
        }}

        /* ── Share ── */
        .share-section {{
            border-top: 1px solid var(--border);
            padding: 40px 0; display: flex; align-items: center; gap: 16px;
        }}
        .share-label {{ font-size: 13px; color: var(--text-dim); }}
        .share-btn {{
            background: var(--surface2); border: 1px solid var(--border);
            color: var(--text); padding: 10px 20px; border-radius: 8px;
            font-size: 14px; cursor: pointer; transition: all 0.2s;
            font-family: inherit;
        }}
        .share-btn:hover {{ border-color: var(--accent); color: var(--accent); }}

        /* ── Bottom CTA ── */
        .bottom-cta {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 16px; padding: 48px; text-align: center;
            max-width: 740px; margin: 0 auto 80px;
        }}
        .bottom-cta h2 {{
            font-family: 'Playfair Display', serif; font-size: 28px;
            margin-bottom: 12px;
        }}
        .bottom-cta p {{ color: var(--text-dim); font-size: 15px; margin-bottom: 24px; }}
        .btn-primary {{
            display: inline-block; background: var(--accent); color: #0f0f0f;
            padding: 14px 32px; border-radius: 8px; font-weight: 600;
            text-decoration: none; transition: all 0.2s; font-size: 15px;
        }}
        .btn-primary:hover {{ background: #f0d45e; text-decoration: none; }}

        /* ── Footer ── */
        footer {{
            border-top: 1px solid var(--border); padding: 32px 40px;
            text-align: center; font-size: 12px; color: var(--text-dim);
        }}
        footer a {{ color: var(--text-dim); }}
        footer a:hover {{ color: var(--accent); }}

        @media (max-width: 640px) {{
            .article-hero, .article-body {{ padding-left: 20px; padding-right: 20px; }}
            .site-header {{ padding: 14px 20px; }}
            .site-nav {{ display: none; }}
        }}
    </style>
</head>
<body>

<!-- Site Header -->
<header class="site-header">
    <a href="https://www.freefonts1001.com/" class="site-logo">FreeFonts<em>1001</em></a>
    <nav class="site-nav">
        <a href="https://www.freefonts1001.com/">Home</a>
        <a href="https://www.freefonts1001.com/">Categories</a>
        <a href="https://www.freefonts1001.com/">Trending</a>
        <a href="https://www.freefonts1001.com/">License Guide</a>
    </nav>
</header>

<!-- Article Hero -->
<article>
    <div class="article-hero">
        <div class="article-meta">
            <span class="article-category">{category}</span>
            <span>{read_time}</span>
            <span>{date_display}</span>
        </div>
        <div class="article-emoji">{emoji}</div>
        <h1>{title}</h1>
        <p class="article-intro">{intro}</p>
        <div class="article-tags">
            {tags_html}
        </div>
    </div>

    <!-- Article Body -->
    <div class="article-body">
        <div class="article-content">
            {sections_html}
        </div>

        <!-- Related Fonts -->
        <div class="related-fonts">
            <h3>🔗 Related Fonts on FreeFonts1001</h3>
            <div class="font-chips">
                {font_chips_html}
            </div>
        </div>

        <!-- Share -->
        <div class="share-section">
            <span class="share-label">Share this story:</span>
            <button class="share-btn" onclick="navigator.clipboard.writeText(window.location.href); this.textContent='✓ Link Copied!'">Copy Link</button>
        </div>
    </div>
</article>

<!-- Bottom CTA -->
<div class="bottom-cta" style="padding: 0 40px 80px; max-width: 860px; margin: 0 auto;">
    <h2>Explore More Free Fonts</h2>
    <p>Browse 15,000+ free fonts for personal and commercial use — updated daily on FreeFonts1001.</p>
    <a href="https://www.freefonts1001.com/" class="btn-primary">Browse All Fonts →</a>
</div>

<!-- Footer -->
<footer>
    <p>© 2026 <a href="https://www.freefonts1001.com/">FreeFonts1001.com</a> · Daily Font Stories · Updated Every Day</p>
</footer>

</body>
</html>"""


# ── 核心函数 ────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """将字符串转为 URL-safe slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text[:60]


def select_topic(date: datetime.date) -> dict:
    """按日期轮换选择主题，保证每天不重复（跨年循环）"""
    index = date.toordinal() % len(TOPICS)
    return TOPICS[index]


def generate_html(topic: dict, date: datetime.date) -> str:
    """将主题数据填充到 HTML 模板"""

    # tags
    tags_html = ''.join(f'<span class="tag">{tag}</span>' for tag in topic['tags'])

    # sections
    sections_html = ''
    for i, sec in enumerate(topic['sections']):
        sections_html += f'''
        <div class="article-section">
            <h2>{sec["heading"]}</h2>
            <p>{sec["body"]}</p>
        </div>'''

    # font chips
    font_chips_html = ''
    for font in topic['related_fonts']:
        font_chips_html += f'<span class="font-chip">✦ {font}</span>'

    # metadata
    meta_desc = topic['intro'][:155] + '...'
    meta_keywords = ', '.join(topic['tags'] + topic['related_fonts'])

    return STORY_TEMPLATE.format(
        lang='en',
        title=topic['title'],
        category=topic['category'],
        emoji=topic['emoji'],
        read_time=topic['read_time'],
        date_display=date.strftime('%B %d, %Y'),
        intro=topic['intro'],
        tags_html=tags_html,
        meta_desc=meta_desc,
        meta_keywords=meta_keywords,
        sections_html=sections_html,
        section_marker=f'{topic["emoji"]} ',
        font_chips_html=font_chips_html,
    )


def git_commit_and_push(html_path: Path, topic: dict, date: datetime.date):
    """执行 git add / commit / push"""
    import subprocess

    commit_msg = (
        f"📝 Daily Story {date.isoformat()}: {topic['category']} — "
        f"{topic['title'][:60]} [skip ci]"
    )

    cmds = [
        ['git', 'add', str(html_path)],
        ['git', 'commit', '-m', commit_msg],
        ['git', 'push', 'origin', 'main'],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[WARN] git {' '.join(cmd)}: {result.stderr.strip()}")
        else:
            print(f"[OK]   git {' '.join(cmd)}")


def update_index_html(date: datetime.date, title: str):
    """
    更新 index.html 中的每日故事横幅，指向新生成的文章。
    """
    index_path = BASE_DIR / 'index.html'
    if not index_path.exists():
        print("[WARN] index.html not found, skipping update")
        return

    content = index_path.read_text(encoding='utf-8')

    # 日期显示格式: "Today's Read · May 15, 2026"
    month_names = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    date_display = f"Today's Read · {month_names[date.month-1]} {date.day}, {date.year}"
    date_str = date.isoformat()
    new_href = f"/instroduce/{date_str}"

    # 替换 href
    old_href_pattern = r'href="/instroduce/\d{4}-\d{2}-\d{2}"'
    new_href_attr = f'href="{new_href}"'
    content_new, n1 = re.subn(old_href_pattern, new_href_attr, content)

    # 替换日期文字
    old_date_pattern = r"Today's Read · \w+ \d{1,2}, \d{4}"
    content_new, n2 = re.subn(old_date_pattern, date_display, content_new)

    # 替换标题（在 daily-story-title 的 div 里）
    old_title_pattern = r'(<div class="daily-story-title">)[^<]+(</div>)'
    content_new, n3 = re.subn(old_title_pattern, r'\g<1>' + title + r'\g<2>', content_new)

    if n1 == 0 and n2 == 0 and n3 == 0:
        print("[WARN] No banner found in index.html, skipping")
        return

    index_path.write_text(content_new, encoding='utf-8')
    print(f"[OK]   Updated index.html banner → {date_str}")

    # git commit index.html
    cmd_add = ['git', 'add', 'index.html']
    cmd_commit = ['git', 'commit', '-m', f'update: index.html daily story banner → {date_str}']
    cmd_push = ['git', 'push', 'origin', 'main']
    for cmd in [cmd_add, cmd_commit, cmd_push]:
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        cmd_str = ' '.join(cmd)
        if result.returncode != 0:
            print(f"[WARN] git {cmd_str}: {result.stderr.strip()}")
        else:
            print(f"[OK]   git {cmd_str}")


def run(date_override: str = None):
    """
    主运行函数：
    1. 选择今日主题
    2. 生成 HTML
    3. 保存文件
    4. git commit & push
    """
    if date_override:
        date = datetime.date.fromisoformat(date_override)
    else:
        date = datetime.date.today()

    topic = select_topic(date)
    html = generate_html(topic, date)

    # 文件名：[YYYY-MM-DD].html
    filename = f"{date.isoformat()}.html"
    html_path = BASE_DIR / filename
    html_path.write_text(html, encoding='utf-8')
    print(f"[OK]   Saved: {html_path} ({len(html):,} bytes)")

    # Git
    try:
        git_commit_and_push(html_path, topic, date)
    except Exception as e:
        print(f"[WARN] Git push failed: {e}")

    # 更新首页横幅
    try:
        update_index_html(date, topic['title'])
    except Exception as e:
        print(f"[WARN] index.html update failed: {e}")

    return html_path, topic, date


if __name__ == '__main__':
    import sys
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    path, topic, date = run(date_arg)
    print(f"\n✅ Done! Generated: {topic['emoji']} {topic['category']} — {topic['title']}")
