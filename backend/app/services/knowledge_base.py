"""
VYRON AI 2.0 — Comprehensive Civic, Legal & Administrative Jargon Knowledge Base
Contains authoritative bilingual (English + Hindi) definitions, citizen contexts,
everyday real-world analogies, and statutory obligations.
"""
import re
from typing import Dict, Any, List, Optional

CIVIC_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # --------------------------------------------------------------------------
    # 1. Municipal Corporation, Property Tax & Urban Governance
    # --------------------------------------------------------------------------
    "tenement": {
        "term": "Tenement (व्यावसायिक / आवासीय भवन)",
        "keywords": ["tenement", "tenements"],
        "simple_meaning": "कर निर्धारण के लिए पंजीकृत दुकान, मकान या व्यावसायिक परिसर (Assessed property unit)",
        "contextual_meaning": "नगर निगम के टैक्स रिकॉर्ड में दर्ज आपकी वह विशिष्ट संपत्ति या दुकान जिस पर बकाया टैक्स की मांग की गई है।",
        "example": "जैसे बिजली विभाग में प्रत्येक मीटर का अलग कनेक्शन नंबर होता है, वैसे ही नगर निगम में टैक्स वसूली के लिए प्रत्येक दुकान या फ्लैट को 'टेनमेंट' कहा जाता है।",
        "action_required": "नोटिस पर दर्ज प्रॉपर्टी खाता संख्या (Property Account No.) का अपने पुराने टैक्स बिल से मिलान करें।"
    },
    "distress warrant": {
        "term": "Distress Warrant (कुर्की वारंट / संपत्ति जब्ती आदेश)",
        "keywords": ["distress warrant", "distress warrants", "distress"],
        "simple_meaning": "टैक्स न भरने पर दुकान/मकान का सामान या बैंक खाता जब्त करने का सरकारी आदेश (Property seizure warrant)",
        "contextual_meaning": "यदि निर्धारित समय सीमा तक टैक्स जमा नहीं किया जाता, तो नगर निगम बिना कोर्ट जाए आपकी संपत्ति कुर्क या सील कर सकता है।",
        "example": "जैसे बैंक लोन न चुकाने पर गाड़ी या दुकान जब्त कर लेता है, वैसे ही सरकारी बकाये की वसूली के लिए नगर निगम आपकी चल-अचल संपत्ति कुर्क कर सकता है।",
        "action_required": "अंतिम तारीख से पहले बकाया राशि जमा करें या अपील दाखिल करके इस कार्रवाई से बचें।"
    },
    "severance": {
        "term": "Severance (सरकारी सेवाओं का विच्छेदन / कनेक्शन काटना)",
        "keywords": ["severance", "severing", "severance of municipal water"],
        "simple_meaning": "नगर निगम द्वारा पानी या जल निकासी का नल कनेक्शन काट देना (Utility disconnection)",
        "contextual_meaning": "प्रॉपर्टी टैक्स न भरने पर नगर निगम आपके परिसर की पानी की पाइपलाइन या सीवर कनेक्शन को काट देगा।",
        "example": "जैसे मोबाइल रिचार्ज न कराने पर सिम कार्ड की सेवाएं बंद हो जाती हैं, वैसे ही टैक्स न देने पर नगरपालिका पानी की आपूर्ति काट देती है।",
        "action_required": "जल आपूर्ति विच्छेदन से बचने के लिए तुरंत जल उपकर व संपत्ति कर का भुगतान करें।"
    },
    "rateable value": {
        "term": "Rateable Value (कर योग्य वार्षिक संपत्ति मूल्यांकन)",
        "keywords": ["rateable value", "ratable value"],
        "simple_meaning": "संपत्ति का अनुमानित वार्षिक किराया जिसके आधार पर टैक्स तय होता है (Annual assessed rental value)",
        "contextual_meaning": "नगर निगम द्वारा आपकी दुकान या मकान के क्षेत्रफल और लोकेशन के आधार पर आंका गया वह मूल्य जिस पर टैक्स का प्रतिशत लगाया जाता है।",
        "example": "जैसे किसी व्यक्ति की कुल वार्षिक आय के आधार पर इनकम टैक्स स्लैब तय होता है, वैसे ही दुकान के रेटएबल वैल्यू से प्रॉपर्टी टैक्स निकलता है।",
        "action_required": "यदि आपको लगता है कि आपकी दुकान का मूल्यांकन बहुत अधिक आंका गया है, तो 21 दिनों में आपत्ति दर्ज करें।"
    },
    "pre-deposit": {
        "term": "Pre-Deposit (अपील से पूर्व अनिवार्य अग्रिम जमा राशि)",
        "keywords": ["pre-deposit", "predeposit"],
        "simple_meaning": "टैक्स के खिलाफ कानूनी शिकायत या अपील दर्ज करने से पहले 50% राशि जमा करने की शर्त",
        "contextual_meaning": "यदि आप टैक्स राशि से असहमत हैं और आपत्ति दर्ज कराना चाहते हैं, तो अपील पर सुनवाई तभी होगी जब आप मांगी गई राशि का 50% पहले जमा कर दें।",
        "example": "जैसे कोर्ट में अपील दायर करने से पहले सिक्योरिटी बॉन्ड जमा करना पड़ता है, वैसे ही सुनवाई शुरू होने से पहले आधा टैक्स जमा करना होगा।",
        "action_required": "फॉर्म 'C' में आपत्ति दर्ज करते समय 50% अग्रिम ड्राफ्ट या रसीद संलग्न करें।"
    },
    "per mensem": {
        "term": "Per Mensem (प्रति माह ब्याज दर)",
        "keywords": ["per mensem", "p.m.", "per month"],
        "simple_meaning": "हर महीने लगने वाला अतिरिक्त ब्याज जुर्माना (2% per month penalty)",
        "contextual_meaning": "तय तारीख के बाद हर महीने 2% का ब्याज जुड़ेगा, जो सालाना 24% हो जाता है।",
        "example": "जैसे किसी साहूकार से लिया गया मासिक ब्याज हर महीने मूलधन में जुड़ता जाता है।",
        "action_required": "जुर्माने के संचय से बचने के लिए 15 अक्टूबर से पहले भुगतान करें।"
    },
    "amenity cess": {
        "term": "Amenity Cess (नागरिक सुविधा उपकर)",
        "keywords": ["amenity cess", "drainage amenity cess", "cess"],
        "simple_meaning": "सड़क, नाली और सफाई सेवाओं के लिए टैक्स के साथ लिया जाने वाला अतिरिक्त सरकारी शुल्क",
        "contextual_meaning": "मूल प्रॉपर्टी टैक्स के अलावा नगर पालिका द्वारा सीवर और नागरिक सुविधाओं के रखरखाव के लिए लगाया गया उपकर।",
        "example": "जैसे होटल बिल में खाने के दाम के ऊपर सर्विस टैक्स और जीएसटी जुड़ता है, वैसे ही टैक्स के ऊपर सेस लगता है।",
        "action_required": "कुल देय राशि में सेस शामिल होता है, अलग से भुगतान करने की आवश्यकता नहीं है।"
    },
    "assessee": {
        "term": "Assessee (करदाता / नोटिस प्राप्तकर्ता)",
        "keywords": ["assessee", "assessees"],
        "simple_meaning": "वह नागरिक, व्यापारी या कंपनी जिस पर कानूनन टैक्स चुकाने का दायित्व है (Taxpayer liable)",
        "contextual_meaning": "इस कानूनी नोटिस में नामजद वह व्यक्ति या फर्म जो इस बकाये के भुगतान के लिए कानूनी रूप से उत्तरदायी है।",
        "example": "जैसे बिजली बिल पर उपभोक्ता का नाम दर्ज होता है, वैसे ही नगर निगम रिकॉर्ड में दर्ज स्वामी 'असेसी' है।",
        "action_required": "सुनिश्चित करें कि नोटिस पर आपका नाम और पता सही दर्ज है।"
    },
    "mmc act": {
        "term": "MMC Act (मुंबई नगर निगम अधिनियम)",
        "keywords": ["mmc act", "section 202", "section 207-a"],
        "simple_meaning": "नगर निगम का वैधानिक कानून जिसके तहत टैक्स वसूली और जब्ती के कानूनी अधिकार प्राप्त हैं",
        "contextual_meaning": "वह सरकारी कानून जो नगर निगम कमिश्नर को बिना कोर्ट गए नोटिस भेजने, जुर्माना लगाने और कुर्की करने की शक्ति देता है।",
        "example": "जैसे मोटर व्हीकल एक्ट के तहत पुलिस चालान काटती है, वैसे ही एमएमसी एक्ट के तहत नगर निगम टैक्स वसूलता है।",
        "action_required": "नोटिस में दी गई धाराओं (धारा 202 व 207-A) का पालन अनिवार्य है।"
    },

    # --------------------------------------------------------------------------
    # 2. University, Higher Education & Examination Regulations
    # --------------------------------------------------------------------------
    "condonation": {
        "term": "Condonation (उपस्थिति की कमी में आधिकारिक छूट / दंड माफ़ी)",
        "keywords": ["condonation", "condone", "attendance condonation"],
        "simple_meaning": "बीमारी के कारण कॉलेज उपस्थिति 75% से कम होने पर विशेष अनुमति देकर परीक्षा देने की अनुमति (Attendance relaxation certificate)",
        "contextual_meaning": "जिन छात्रों की उपस्थिति 60% से 74.9% के बीच है, वे मेडिकल पर्ची और ₹1,500 जुर्माना देकर परीक्षा में बैठने की छूट पा सकते हैं।",
        "example": "जैसे ऑफिस में छुट्टी की कमी होने पर मेडिकल सर्टिफिकेट देकर सिक लीव स्वीकृत कराई जाती है, वैसे ही यह परीक्षा में बैठने का अनुमति पत्र है।",
        "action_required": "25 अक्टूबर शाम 5 बजे से पहले समर्थ पोर्टल पर मेडिकल हलफनामा और ₹1,500 शुल्क जमा करें।"
    },
    "debarment": {
        "term": "Debarment (परीक्षा से निष्कासन / वंचित करना)",
        "keywords": ["debarment", "debarred", "precluded"],
        "simple_meaning": "छात्र को परीक्षा में बैठने से रोक देना और एडमिट कार्ड जारी न करना (Disqualification from exams)",
        "contextual_meaning": "यदि उपस्थिति की कमी को माफ नहीं कराया गया, तो छात्र आगामी शीतकालीन परीक्षा (Winter Exam) में नहीं बैठ पाएगा।",
        "example": "जैसे बिना टिकट यात्री को स्टेशन पर ट्रेन में चढ़ने से रोक दिया जाता है, वैसे ही छात्र को परीक्षा केंद्र में नहीं जाने दिया जाएगा।",
        "action_required": "परीक्षा से निष्कासन से बचने के लिए अंतिम तारीख से पहले आवेदन स्वीकृत कराएं।"
    },
    "provisional abeyance": {
        "term": "Provisional Abeyance (अस्थायी रोक / छात्रवृत्ति का निलंबन)",
        "keywords": ["provisional abeyance", "abeyance"],
        "simple_meaning": "अनुशासनात्मक जांच पूरी होने तक छात्रवृत्ति या लाभ का पैसा रोक कर रखना (Put on hold)",
        "contextual_meaning": "डिबार होने की स्थिति में छात्र को मिलने वाली सरकारी मेरिट स्कॉलरशिप का वितरण अस्थायी रूप से फ्रीज कर दिया जाएगा।",
        "example": "जैसे बैंक खाते में कोई समस्या होने पर सरकारी सब्सिडी का पैसा कुछ समय के लिए होल्ड पर चला जाता है।",
        "action_required": "उपस्थिति प्रमाण पत्र जमा करके अपना स्कॉलरशिप खाता तुरंत पुनः सक्रिय कराएं।"
    },
    "pedagogical module": {
        "term": "Pedagogical Module (शैक्षणिक विषय / पाठ्यक्रम पेपर)",
        "keywords": ["pedagogical module", "pedagogical modules", "pedagogical"],
        "simple_meaning": "डिग्री या सेमेस्टर का प्रत्येक विषय या थ्योरी/प्रैक्टिकल कोर्स (Subject paper in syllabus)",
        "contextual_meaning": "छात्र को केवल कुल उपस्थिति में नहीं, बल्कि हर विषय में अलग-अलग 75% बायोमेट्रिक उपस्थिति पूरी करनी होगी।",
        "example": "जैसे 5 विषयों की परीक्षा में हर विषय में अलग-अलग पास होना जरूरी होता है, वैसे ही हर मॉड्यूल में 75% उपस्थिति अनिवार्य है।",
        "action_required": "विषयवार अपनी बायोमेट्रिक उपस्थिति की जांच पोर्टल पर करें।"
    },
    "non-judicial stamp paper": {
        "term": "Non-Judicial Stamp Paper (गैर-न्यायिक स्टाम्प पेपर)",
        "keywords": ["non-judicial stamp paper", "stamp paper"],
        "simple_meaning": "शपथ पत्र (Affidavit) बनवाने के लिए उपयोग किया जाने वाला सरकारी स्टाम्प पेपर",
        "contextual_meaning": "कॉलेज में बीमारी का कारण बताने के लिए नोटरी या वकील से ₹100 के स्टाम्प पेपर पर एफिडेविट बनवाना अनिवार्य है।",
        "example": "जैसे किराया समझौता (Rent Agreement) स्टाम्प पेपर पर बनता है, वैसे ही यह कानूनी शपथ पत्र है।",
        "action_required": "वकील या कोर्ट नोटरी से शपथ पत्र बनवाकर समर्थ पोर्टल पर स्कैन कॉपी अपलोड करें।"
    },
    "admit card": {
        "term": "Admit Card / Hall Ticket (परीक्षा प्रवेश पत्र)",
        "keywords": ["admit card", "hall ticket"],
        "simple_meaning": "परीक्षा हॉल में प्रवेश के लिए अनिवार्य आधिकारिक पहचान पत्र (Exam entry pass)",
        "contextual_meaning": "वह मूल कार्ड जिसके बिना किसी भी परीक्षार्थी को परीक्षा भवन में प्रवेश नहीं दिया जाता।",
        "example": "जैसे सिनेमा हॉल या हवाई जहाज में बोर्डिंग पास के बिना प्रवेश नहीं मिलता, वैसे ही परीक्षा में एडमिट कार्ड जरूरी है।",
        "action_required": "कंडोनेशन प्रक्रिया पूरी करने के बाद ही पोर्टल से एडमिट कार्ड डाउनलोड हो सकेगा।"
    },

    # --------------------------------------------------------------------------
    # 3. Banking, RBI Directives & Anti-Money Laundering (KYC)
    # --------------------------------------------------------------------------
    "re-kyc": {
        "term": "Re-KYC (पुनः ग्राहक सत्यापन / पहचान नवीनीकरण)",
        "keywords": ["re-kyc", "periodic kyc", "kyc updation"],
        "simple_meaning": "बैंक खाते को चालू रखने के लिए आधार, पैन और पते का प्रमाण दोबारा जमा करना (Identity re-verification)",
        "contextual_meaning": "आरबीआई नियमों के तहत बैंक को हर कुछ वर्षों में खाताधारक की नई फोटो और वर्तमान पते का नवीनीकरण करना अनिवार्य है।",
        "example": "जैसे ड्राइविंग लाइसेंस की मियाद खत्म होने पर उसे रिन्यू कराना पड़ता है, वैसे ही बैंक खाते का री-केवाईसी होता है।",
        "action_required": "31 अक्टूबर से पहले बैंक शाखा में या बैंकिंग ऐप से आधार और पैन कार्ड अपलोड करें।"
    },
    "debit freeze": {
        "term": "Debit Freeze (खाते से पैसे निकालने पर पूर्ण रोक)",
        "keywords": ["debit freeze", "freeze", "freezing"],
        "simple_meaning": "खाते से यूपीआई, एटीएम, चेक या नेट बैंकिंग द्वारा पैसे निकालने पर रोक लगा देना (Account withdrawal block)",
        "contextual_meaning": "तय तारीख तक री-केवाईसी न कराने पर आप अपने खाते से पैसे नहीं निकाल सकेंगे, न ही यूपीआई चलेगा, हालांकि खाते में पैसे आ सकते हैं।",
        "example": "जैसे तिजोरी में पैसे डाले तो जा सकते हैं लेकिन चाबी बंद होने के कारण निकाले नहीं जा सकते।",
        "action_required": "फ्रीज होने से पहले तुरंत केवाईसी दस्तावेज़ जमा करके खाता चालू रखें।"
    },
    "pmla": {
        "term": "PMLA (धन शोधन निवारण अधिनियम / Prevention of Money Laundering Act)",
        "keywords": ["pmla", "prevention of money laundering act"],
        "simple_meaning": "काले धन और अज्ञात खातों की रोकथाम के लिए भारत सरकार का कड़ा कानून",
        "contextual_meaning": "इस कानून के तहत प्रत्येक बैंक के लिए अपने ग्राहकों की पहचान सत्यापित रखना अनिवार्य है, ऐसा न करने पर खाता बंद हो जाता है।",
        "example": "जैसे सिम कार्ड जारी करने से पहले सरकार पहचान पत्र अनिवार्य करती है ताकि फर्जी सिम न चले।",
        "action_required": "वैध सरकारी पहचान पत्र (आधार / पासपोर्ट / वोटर आईडी) जमा करें।"
    },
    "section 35a": {
        "term": "Section 35A (बैंकिंग विनियमन अधिनियम की धारा 35A)",
        "keywords": ["section 35a", "banking regulation act"],
        "simple_meaning": "रिजर्व बैंक (RBI) का वह कानूनी अधिकार जिसके तहत वह सभी बैंकों को कड़े निर्देश जारी करता है",
        "contextual_meaning": "आरबीआई द्वारा जनहित और बैंकिंग सुरक्षा में जारी किए गए अनिवार्य नियम जिनका पालन बैंक और ग्राहक दोनों को करना होता है।",
        "example": "जैसे ट्रैफिक पुलिस मोटर नियमों के तहत नियम बनाती है और सभी गाड़ियों को उसका पालन करना होता है।",
        "action_required": "यह नोटिस आरबीआई के कानूनी निर्देशों के तहत जारी हुआ है, इसे नजरअंदाज न करें।"
    },
    "standing instruction": {
        "term": "Standing Instruction / NACH (स्वतः भुगतान निर्देश / ईएमआई ऑटो-डेबिट)",
        "keywords": ["standing instructions", "standing instruction", "nach"],
        "simple_meaning": "हर महीने तय तारीख पर बैंक खाते से लोन की किस्त या बिल कटने की स्वचालित सुविधा",
        "contextual_meaning": "यदि खाता डेबिट फ्रीज हो गया, तो आपकी होम लोन, कार लोन या बीमा की ईएमआई बाउंस हो जाएगी और बैंक जुर्माना लगाएगा।",
        "example": "जैसे नेटफ्लिक्स या बिजली का बिल हर महीने अपने आप खाते से कट जाता है।",
        "action_required": "ईएमआई बाउंस पेनल्टी और सिबिल स्कोर खराब होने से बचने के लिए तुरंत खाता चालू कराएं।"
    },
    "form 60": {
        "term": "Form 60 (पैन कार्ड न होने पर स्व-घोषणा पत्र)",
        "keywords": ["form 60"],
        "simple_meaning": "यदि आपके पास पैन कार्ड (PAN Card) नहीं है, तो बैंक में दिया जाने वाला स्व-घोषणा पत्र",
        "contextual_meaning": "वह सरकारी फॉर्म जो उन नागरिकों द्वारा भरा जाता है जिनके पास पैन कार्ड नहीं है और जिनकी आय कर योग्य सीमा से कम है।",
        "example": "जैसे पैन कार्ड न होने पर दिया जाने वाला शपथ पत्र।",
        "action_required": "पैन कार्ड न होने पर बैंक से फॉर्म 60 लेकर भरकर जमा करें।"
    },
    "self-attested": {
        "term": "Self-Attested (स्व-प्रमाणित / स्वयं के हस्ताक्षर युक्त)",
        "keywords": ["self-attested", "self attested"],
        "simple_meaning": "दस्तावेज़ की फोटोकॉपी पर अपने स्वयं के हस्ताक्षर करके उसे प्रमाणित करना",
        "contextual_meaning": "आधार कार्ड या पते के प्रमाण की फोटोकॉपी के नीचे अपने हस्ताक्षर और तारीख लिखकर बैंक में जमा करना।",
        "example": "फोटोकॉपी के नीचे 'Self Attested' लिखकर अपने दस्तखत करना।",
        "action_required": "दस्तावेज़ों की फोटोकॉपी पर साइन करके ही शाखा में जमा करें।"
    },

    # --------------------------------------------------------------------------
    # 4. Court, Police, Legal & Administrative Terminology
    # --------------------------------------------------------------------------
    "show cause notice": {
        "term": "Show Cause Notice (कारण बताओ नोटिस)",
        "keywords": ["show cause notice", "show cause"],
        "simple_meaning": "अधिकारी द्वारा पूछा गया आधिकारिक सवाल कि 'आपके खिलाफ कार्रवाई क्यों न की जाए?' (Notice to explain)",
        "contextual_meaning": "विभाग द्वारा दी गई अंतिम चेतावनी जिसमें आपको लिखित में अपनी सफाई देने का मौका दिया जाता है।",
        "example": "जैसे स्कूल में गलती होने पर प्रिंसिपल द्वारा छात्र से लिखित स्पष्टीकरण मांगना।",
        "action_required": "दी गई समय सीमा के भीतर कानूनी रूप से सही स्पष्टीकरण पत्र दाखिल करें।"
    },
    "ex-parte": {
        "term": "Ex-Parte (एकतरफा आदेश / अनुपस्थिति में दिया गया फैसला)",
        "keywords": ["ex-parte", "ex parte"],
        "simple_meaning": "दूसरी पार्टी के पेश न होने पर केवल उपस्थित पक्ष की बात सुनकर दिया गया फैसला",
        "contextual_meaning": "यदि आप नोटिस के बाद सुनवाई में नहीं पहुंचते, तो अधिकारी आपकी गैर-मौजूदगी में आपके खिलाफ एकतरफा आदेश पारित कर देगा।",
        "example": "जैसे मैच में दूसरी टीम न आने पर पहली टीम को वॉकओवर देकर विजेता घोषित कर दिया जाता है।",
        "action_required": "एकतरफा कार्रवाई से बचने के लिए स्वयं या अपने प्रतिनिधि के माध्यम से उपस्थित हों।"
    },
    "caveat": {
        "term": "Caveat (कैविएट / पूर्व सूचना का कानूनी अधिकार)",
        "keywords": ["caveat", "caveat petition"],
        "simple_meaning": "कोर्ट में दी गई अर्जी कि 'मेरा पक्ष सुने बिना मेरे खिलाफ कोई स्टे या आदेश न दिया जाए'",
        "contextual_meaning": "किसी विवाद में अपने अधिकारों की रक्षा के लिए कोर्ट में पहले से दर्ज की गई चेतावनी याचिका।",
        "example": "जैसे किसी फैसले से पहले अधिकारी को सतर्क करना कि दूसरा पक्ष गलत जानकारी दे सकता है।",
        "action_required": "संबंधित मामले में अदालत के नोटिस पर तुरंत वकील से परामर्श लें।"
    },
    "statutory": {
        "term": "Statutory (कानूनी / कानून द्वारा अनिवार्य)",
        "keywords": ["statutory", "statutory demand", "statutory dues"],
        "simple_meaning": "संसद या विधानसभा द्वारा बनाए गए लिखित कानून के तहत अनिवार्य (Legally binding under statute)",
        "contextual_meaning": "यह कोई साधारण या वैकल्पिक पत्र नहीं है; यह एक सरकारी कानून के तहत जारी हुआ है जिसका उल्लंघन दंडनीय है।",
        "example": "जैसे हेलमेट पहनना मोटर कानून के तहत 'स्टैच्यूटरी' (कानूनी रूप से अनिवार्य) है।",
        "action_required": "दस्तावेज़ में दिए गए निर्देशों का पूर्ण कानूनी अनुपालन करें।"
    },
    "incur": {
        "term": "Incur (जुर्माने का भागी बनना / देनदारी पैदा होना)",
        "keywords": ["incur", "incurred", "shall attract"],
        "simple_meaning": "नियम तोड़ने पर अतिरिक्त आर्थिक दंड या कानूनी जिम्मेदारी अपने ऊपर ले लेना",
        "contextual_meaning": "अंतिम तारीख के बाद पेनल्टी या ब्याज खुद-ब-खुद आपके बकाये में जुड़ जाएगा।",
        "example": "जैसे लेट फीस का भागी बनना।",
        "action_required": "अंतिम तिथि से पहले भुगतान करें।"
    },
    "indemnity": {
        "term": "Indemnity (क्षतिपूर्ति का वचन / हर्जाने की गारंटी)",
        "keywords": ["indemnity", "indemnify", "indemnity bond"],
        "simple_meaning": "किसी नुकसान या गलती की भरपाई स्वयं करने का कानूनी वचन पत्र",
        "contextual_meaning": "संस्था को किसी भी भविष्य के नुकसान या कानूनी विवाद से सुरक्षित रखने के लिए दिया जाने वाला क्षतिपूर्ति बॉन्ड।",
        "example": "जैसे डुप्लीकेट चेक या बॉन्ड जारी कराने के लिए बैंक में क्षतिपूर्ति बॉन्ड देना होता है।",
        "action_required": "शर्तों को ध्यानपूर्वक पढ़कर ही इंडेम्निटी बॉन्ड पर हस्ताक्षर करें।"
    },
    "stay order": {
        "term": "Stay Order (स्थगनादेश / कार्रवाई पर कोर्ट की रोक)",
        "keywords": ["stay order", "interim stay", "stay"],
        "simple_meaning": "कोर्ट द्वारा किसी आदेश, नोटिस या जब्ती पर लगाई गई कानूनी रोक",
        "contextual_meaning": "अदालत का वह अंतरिम आदेश जो नगर निगम या विभाग की कार्रवाई को सुनवाई पूरी होने तक रोक देता है।",
        "example": "जैसे मैच में बारिश होने पर खेल को 'स्टॉप' कर दिया जाता है।",
        "action_required": "स्टे आर्डर की प्रमाणित कॉपी संबंधित विभाग को तुरंत रिसीव कराएं।"
    },

    # --------------------------------------------------------------------------
    # 6. Essential Academic, Notice & Citizen Vocabulary
    # --------------------------------------------------------------------------
    "study": {
        "term": "Study (पढ़ना / अध्ययन करना / पढ़ाई)",
        "keywords": ["study", "studies", "studying"],
        "simple_meaning": "पढ़ना, सीखना या किसी विषय का ज्ञान प्राप्त करना (To read, learn, or examine)",
        "contextual_meaning": "परीक्षा या शैक्षणिक पाठ्यक्रम की तैयारी के लिए किताबों और सामग्री का अध्ययन करना।",
        "example": "जैसे परीक्षा में पास होने और अच्छे अंक लाने के लिए छात्र रोज़ शाम को पढ़ाई (study) करते हैं।",
        "action_required": "परीक्षा की तैयारी के लिए अपने पाठ्यक्रम का नियमित अध्ययन जारी रखें।"
    },
    "postpone": {
        "term": "Postpone / Postponed (स्थगित / आगे की तारीख के लिए टालना)",
        "keywords": ["postpone", "postponed", "postponement", "defer", "deferred"],
        "simple_meaning": "किसी निर्धारित परीक्षा, बैठक या कार्यक्रम को आगे की नई तारीख तक टाल देना (Rescheduled)",
        "contextual_meaning": "वर्तमान तारीख पर यह कार्यक्रम या परीक्षा नहीं होगी; अगली नई तारीख की घोषणा बाद में की जाएगी।",
        "example": "जैसे भारी बारिश के कारण आज का मैच अगले हफ्ते के लिए टाल (Postpone) दिया जाए।",
        "action_required": "नई परीक्षा तिथि की घोषणा के लिए आधिकारिक पोर्टल पर नज़र रखें।"
    },
    "examination": {
        "term": "Examination / Exam (परीक्षा / इम्तिहान)",
        "keywords": ["examination", "exam", "exams", "examinations"],
        "simple_meaning": "छात्रों की योग्यता और समझ की आधिकारिक जांच (Academic test / evaluation)",
        "contextual_meaning": "सेमेस्टर या वर्ष के अंत में होने वाली विश्वविद्यालय या बोर्ड की आधिकारिक परीक्षा।",
        "example": "जैसे अगली कक्षा में जाने के लिए बोर्ड परीक्षा या वार्षिक एग्जाम देना होता है।",
        "action_required": "समय पर एडमिट कार्ड प्राप्त करें और परीक्षा केंद्र पर पहचान पत्र लेकर जाएं।"
    },
    "further notice": {
        "term": "Until Further Notice (अगले आदेश / सूचना तक)",
        "keywords": ["further notice", "until further notice"],
        "simple_meaning": "जब तक विभाग या विश्वविद्यालय द्वारा अगली नई आधिकारिक सूचना जारी नहीं की जाती तब तक",
        "contextual_meaning": "वर्तमान निर्णय (जैसे परीक्षा का टलना) तब तक प्रभावी रहेगा जब तक नया आदेश न आ जाए।",
        "example": "जैसे 'दुकान अगले आदेश तक बंद रहेगी' — यानी जब तक मालिक नया नोटिस न दे, दुकान नहीं खुलेगी।",
        "action_required": "नई तिथि की घोषणा की प्रतीक्षा करें और आधिकारिक ईमेल चेक करते रहें।"
    },
    "penalty": {
        "term": "Penalty (जुर्माना / दंड शुल्क)",
        "keywords": ["penalty", "penalties", "fine", "penal"],
        "simple_meaning": "नियम तोड़ने या अंतिम तिथि के बाद काम करने पर लगने वाला अतिरिक्त आर्थिक दंड (Late fee / fine)",
        "contextual_meaning": "यदि समय सीमा तक फीस या टैक्स नहीं भरा गया, तो मूल राशि के ऊपर अतिरिक्त जुर्माना लगेगा।",
        "example": "जैसे बिना हेलमेट बाइक चलाने पर ट्रैफिक पुलिस चालान (जुर्माना) काटती है।",
        "action_required": "जुर्माने से बचने के लिए अंतिम तिथि से पहले अनिवार्य भुगतान पूरा करें।"
    },
    "admit card": {
        "term": "Admit Card / Hall Ticket (परीक्षा प्रवेश पत्र)",
        "keywords": ["admit card", "hall ticket", "entry pass"],
        "simple_meaning": "परीक्षा हॉल में प्रवेश पाने के लिए आधिकारिक अनुमति पत्र (Exam hall entry ticket)",
        "contextual_meaning": "छात्र का रोल नंबर और परीक्षा केंद्र दर्शाने वाला अनिवार्य प्रवेश पत्र जिसके बिना परीक्षा में नहीं बैठ सकते।",
        "example": "जैसे सिनेमा हॉल में जाने के लिए मूवी टिकट आवश्यक होता है, वैसे ही एग्जाम में एडमिट कार्ड अनिवार्य है।",
        "action_required": "विश्वविद्यालय पोर्टल से समय पर एडमिट कार्ड डाउनलोड कर प्रिंट निकाल लें।"
    },
    "arrears": {
        "term": "Arrears (पिछला बकाया / देय राशि)",
        "keywords": ["arrears", "dues", "outstanding"],
        "simple_meaning": "पिछली तिथियों का वह पैसा या बिल जो समय पर नहीं चुकाया गया और अब बकाया है (Overdue payment)",
        "contextual_meaning": "पुराने महीनों या वर्षों का अनपेड टैक्स या फीस जो इस नोटिस में तत्काल मांगी गई है।",
        "example": "जैसे पिछले तीन महीनों का बिजली बिल न भरने पर वह 'एरियर्स' (बकाया) के रूप में जुड़कर आता है।",
        "action_required": "बकाया राशि का तुरंत भुगतान करें ताकि ब्याज और सेवा विच्छेदन से बचा जा सके।"
    },
    "compliance": {
        "term": "Compliance (अनुपालन / नियमों का कड़ाई से पालन)",
        "keywords": ["compliance", "comply", "compliant"],
        "simple_meaning": "सरकारी या संस्थागत नियमों और कानूनों के अनुसार कार्य करना (Following the rules)",
        "contextual_meaning": "नोटिस में दिए गए निर्देशों और शर्तों को समय सीमा के भीतर पूरा करने की वैधानिक बाध्यता।",
        "example": "जैसे सड़क पर लाल बत्ती पर रुकना ट्रैफिक नियमों का अनुपालन (Compliance) है।",
        "action_required": "नोटिस की सभी शर्तों को समय पर पूरा कर विभाग में पावती जमा करें।"
    }
}

def lookup_term(term: str) -> Optional[Dict[str, Any]]:
    """Looks up a statutory or civic term in the authoritative knowledge base."""
    if not term:
        return None
    t_clean = term.strip().lower()
    
    # Exact or keyword match
    for key, data in CIVIC_KNOWLEDGE_BASE.items():
        if t_clean == key or t_clean in data.get("keywords", []):
            return data
        # Check substring match
        if any(kw in t_clean for kw in data.get("keywords", [])):
            return data
            
    return None

def extract_known_terms(document_text: str) -> List[Dict[str, Any]]:
    """
    Scans a document and extracts all recognized civic, legal, and statutory terms
    with complete verified bilingual explanations, analogies, and action items.
    """
    found_terms = []
    seen_keys = set()
    text_lower = document_text.lower()

    for key, data in CIVIC_KNOWLEDGE_BASE.items():
        matched = False
        for kw in data.get("keywords", []):
            pattern = rf"\b{re.escape(kw)}\b"
            if re.search(pattern, text_lower):
                matched = True
                break

        if matched and key not in seen_keys:
            seen_keys.add(key)
            # Find the sentence containing this term for context
            sentence_match = re.search(rf"([^.?!।\n]*\b(?:{'|'.join(re.escape(k) for k in data['keywords'])})\b[^.?!।\n]*[.?!।])", document_text, re.IGNORECASE)
            source_sent = sentence_match.group(1).strip() if sentence_match else f"Mentioned in document context."

            found_terms.append({
                "term": data["term"],
                "simple_meaning": data["simple_meaning"],
                "contextual_meaning": data["contextual_meaning"],
                "example": data["example"],
                "source_sentence": source_sent,
                "action_required": data.get("action_required", "")
            })

    return found_terms

def get_knowledge_base_prompt_snippet() -> str:
    """Returns a dense prompt context for LLMs containing key civic terminology."""
    lines = ["AUTHORITATIVE CIVIC JARGON KNOWLEDGE BASE (Use these verified meanings):"]
    for key, item in list(CIVIC_KNOWLEDGE_BASE.items())[:15]:
        lines.append(f"- {key.upper()}: {item['simple_meaning']} | Context: {item['contextual_meaning']} | Analogy: {item['example']}")
    return "\n".join(lines)
