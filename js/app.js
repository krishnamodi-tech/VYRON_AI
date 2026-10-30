/**
 * VYRON AI 2.0 — Comprehensive Client Application Orchestrator
 * Multilingual Public Document Simplifier, Jargon Decoder & Grounded Q&A Platform
 */

// Application Global State
const state = {
    backendUrl: (() => {
        if (window.VYRON_API_URL) return window.VYRON_API_URL;
        if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
            return `${location.protocol}//${location.hostname}:8000`;
        }
        return location.origin;
    })(),
    isBackendOnline: false,
    aiProvider: "none",
    activeModel: "",
    currentTab: "paneText",
    selectedFile: null,
    extractedSourceText: "",
    lastAnalysisData: null,
    speechUtterance: null,
    speechIsPaused: false,
    cameraFacingMode: "environment", // "environment" or "user"
    cameraStream: null
};

// Built-in Authoritative Civic & Legal Knowledge Base Dictionary
const CIVIC_CLIENT_DICTIONARY = {
    "tenement": {
        term: "Tenement (व्यावसायिक / आवासीय भवन)",
        simple_meaning: "कर निर्धारण के लिए पंजीकृत दुकान, मकान या व्यावसायिक परिसर (Property unit)",
        contextual_meaning: "नगर निगम के टैक्स रिकॉर्ड में दर्ज आपकी वह विशिष्ट दुकान या फ्लैट जिस पर बकाया टैक्स मांगा गया है।",
        example: "जैसे बिजली बिल प्रत्येक मीटर नंबर पर आता है, वैसे ही नगर निगम में प्रत्येक कर-योग्य दुकान को 'टेनमेंट' कहते हैं।"
    },
    "distress warrant": {
        term: "Distress Warrant (कुर्की वारंट / संपत्ति जब्ती आदेश)",
        simple_meaning: "टैक्स न भरने पर दुकान का सामान या बैंक खाता कुर्क करने का सरकारी आदेश (Property seizure warrant)",
        contextual_meaning: "यदि निर्धारित समय सीमा तक टैक्स जमा नहीं किया जाता, तो नगर निगम बिना कोर्ट जाए आपकी संपत्ति कुर्क या सील कर सकता है।",
        example: "जैसे बैंक लोन न चुकाने पर गाड़ी जब्त कर लेता है, वैसे ही सरकारी बकाये के लिए नगर निगम सामान कुर्क कर सकता है।"
    },
    "severance": {
        term: "Severance (सरकारी सेवाओं का विच्छेदन / कनेक्शन काटना)",
        simple_meaning: "नगर निगम द्वारा पानी या सीवर का नल कनेक्शन काट देना (Utility disconnection)",
        contextual_meaning: "प्रॉपर्टी टैक्स न भरने पर नगर निगम आपके परिसर की पानी की पाइपलाइन काट देगा।",
        example: "जैसे फोन रिचार्ज न कराने पर सिम कार्ड की सेवाएं बंद हो जाती हैं।"
    },
    "rateable value": {
        term: "Rateable Value (कर योग्य वार्षिक संपत्ति मूल्यांकन)",
        simple_meaning: "संपत्ति का अनुमानित वार्षिक किराया जिसके आधार पर टैक्स तय होता है (Annual assessed rental value)",
        contextual_meaning: "नगर निगम द्वारा दुकान के क्षेत्रफल और लोकेशन के आधार पर आंका गया वह मूल्य जिस पर टैक्स का प्रतिशत लगाया जाता है।",
        example: "जैसे कर्मचारी की सैलरी के आधार पर इनकम टैक्स स्लैब तय होता है।"
    },
    "per mensem": {
        term: "Per Mensem (प्रति माह ब्याज दर)",
        simple_meaning: "हर महीने लगने वाला अतिरिक्त ब्याज जुर्माना (2% per month interest)",
        contextual_meaning: "तय तारीख के बाद हर महीने 2% का ब्याज जुड़ेगा, जो सालाना 24% हो जाता है।",
        example: "जैसे किसी साहूकार से लिया गया मासिक ब्याज हर महीने मूलधन में जुड़ता जाता है।"
    },
    "pre-deposit": {
        term: "Pre-Deposit (अपील से पूर्व अनिवार्य अग्रिम जमा राशि)",
        simple_meaning: "टैक्स के खिलाफ कानूनी शिकायत या अपील दर्ज करने से पहले 50% राशि जमा करने की शर्त",
        contextual_meaning: "यदि आप टैक्स राशि से असहमत हैं और आपत्ति दर्ज कराना चाहते हैं, तो अपील पर सुनवाई तभी होगी जब आप मांगी गई राशि का 50% पहले जमा कर दें।",
        example: "जैसे कोर्ट में सुनवाई शुरू होने से पहले सिक्योरिटी ड्राफ्ट जमा करना पड़ता है।"
    },
    "condonation": {
        term: "Condonation (उपस्थिति की कमी में छूट / दंड माफ़ी प्रमाण पत्र)",
        simple_meaning: "बीमारी के कारण कॉलेज उपस्थिति 75% से कम होने पर विशेष अनुमति देकर परीक्षा देने की छूट (Attendance relaxation)",
        contextual_meaning: "जिन छात्रों की उपस्थिति 60% से 74.9% है, वे मेडिकल पर्ची और ₹1,500 शुल्क देकर परीक्षा में बैठने की छूट पा सकते हैं।",
        example: "जैसे डॉक्टर की पर्ची देने पर सिक लीव स्वीकृत होती है, वैसे ही यह परीक्षा अनुमति पत्र है।"
    },
    "debarment": {
        term: "Debarment (परीक्षा से निष्कासन / वंचित करना)",
        simple_meaning: "छात्र को परीक्षा में बैठने से रोक देना और एडमिट कार्ड जारी न करना (Disqualification)",
        contextual_meaning: "यदि उपस्थिति की कमी को माफ नहीं कराया गया, तो छात्र आगामी शीतकालीन परीक्षा (Winter Exam) में नहीं बैठ पाएगा।",
        example: "जैसे बिना टिकट यात्री को स्टेशन पर ट्रेन में चढ़ने से रोक दिया जाता है।"
    },
    "provisional abeyance": {
        term: "Provisional Abeyance (अस्थायी रोक / छात्रवृत्ति का निलंबन)",
        simple_meaning: "अनुशासनात्मक जांच पूरी होने तक छात्रवृत्ति या लाभ का पैसा रोक कर रखना (Put on hold)",
        contextual_meaning: "डिबार होने की स्थिति में छात्र को मिलने वाली सरकारी मेरिट स्कॉलरशिप का वितरण अस्थायी रूप से फ्रीज कर दिया जाएगा।",
        example: "जैसे बैंक खाते में कोई समस्या होने पर सरकारी सब्सिडी का पैसा कुछ समय के लिए होल्ड पर चला जाता है।"
    },
    "re-kyc": {
        term: "Re-KYC (पुनः ग्राहक सत्यापन / पहचान नवीनीकरण)",
        simple_meaning: "बैंक खाते को चालू रखने के लिए आधार, पैन और पते का प्रमाण दोबारा जमा करना (Identity re-verification)",
        contextual_meaning: "आरबीआई नियमों के तहत बैंक को हर कुछ वर्षों में खाताधारक की नई फोटो और वर्तमान पते का नवीनीकरण करना अनिवार्य है।",
        example: "जैसे ड्राइविंग लाइसेंस की मियाद खत्म होने पर उसे रिन्यू कराना पड़ता है।"
    },
    "debit freeze": {
        term: "Debit Freeze (खाते से पैसे निकालने पर पूर्ण रोक)",
        simple_meaning: "खाते से यूपीआई, एटीएम, चेक या नेट बैंकिंग द्वारा पैसे निकालने पर रोक लगा देना (Account withdrawal block)",
        contextual_meaning: "तय तारीख तक री-केवाईसी न कराने पर आप अपने खाते से पैसे नहीं निकाल सकेंगे, हालांकि खाते में पैसे आ सकते हैं।",
        example: "जैसे तिजोरी में पैसे डाले तो जा सकते हैं लेकिन चाबी बंद होने के कारण निकाले नहीं जा सकते।"
    },
    "pmla": {
        term: "PMLA (धन शोधन निवारण अधिनियम)",
        simple_meaning: "काले धन और अज्ञात खातों की रोकथाम के लिए भारत सरकार का कड़ा कानून",
        contextual_meaning: "इस कानून के तहत प्रत्येक बैंक के लिए अपने ग्राहकों की पहचान सत्यापित रखना अनिवार्य है।",
        example: "जैसे सिम कार्ड जारी करने से पहले सरकार पहचान पत्र अनिवार्य करती है ताकि फर्जी सिम न चले।"
    },
    "statutory": {
        term: "Statutory (कानूनी / कानून द्वारा अनिवार्य)",
        simple_meaning: "संसद या विधानसभा द्वारा बनाए गए लिखित कानून के तहत अनिवार्य",
        contextual_meaning: "यह कोई साधारण या वैकल्पिक पत्र नहीं है; यह एक सरकारी कानून के तहत जारी हुआ है जिसका उल्लंघन दंडनीय है।",
        example: "जैसे हेलमेट पहनना मोटर कानून के तहत अनिवार्य है।"
    },
    "study": {
        term: "Study (पढ़ना / अध्ययन करना / पढ़ाई)",
        simple_meaning: "पढ़ना, सीखना या किसी विषय का ज्ञान प्राप्त करना (To read, learn, or examine)",
        contextual_meaning: "परीक्षा या शैक्षणिक पाठ्यक्रम की तैयारी के लिए किताबों और सामग्री का अध्ययन करना।",
        example: "जैसे परीक्षा में पास होने और अच्छे अंक लाने के लिए छात्र रोज़ शाम को पढ़ाई (study) करते हैं।"
    },
    "postpone": {
        term: "Postpone / Postponed (स्थगित / आगे की तारीख के लिए टालना)",
        simple_meaning: "किसी निर्धारित परीक्षा, बैठक या कार्यक्रम को आगे की नई तारीख तक टाल देना (Rescheduled)",
        contextual_meaning: "वर्तमान तारीख पर यह कार्यक्रम या परीक्षा नहीं होगी; अगली नई तारीख की घोषणा बाद में की जाएगी।",
        example: "जैसे भारी बारिश के कारण आज का मैच अगले हफ्ते के लिए टाल (Postpone) दिया जाए।"
    },
    "postponed": {
        term: "Postponed (स्थगित / टाल दिया गया)",
        simple_meaning: "परीक्षा या कार्यक्रम की तिथि को आगे बढ़ा दिया गया है (Deferred to a later date)",
        contextual_meaning: "वर्तमान घोषित तारीख पर यह प्रक्रिया नहीं होगी; नई तिथि की अलग से घोषणा होगी।",
        example: "जैसे परीक्षा की तारीख आगे बढ़ा देना (Exam Postponed होना)।"
    },
    "examination": {
        term: "Examination / Exam (परीक्षा / इम्तिहान)",
        simple_meaning: "छात्रों की योग्यता और समझ की आधिकारिक जांच (Academic evaluation test)",
        contextual_meaning: "सेमेस्टर या वर्ष के अंत में होने वाली विश्वविद्यालय या बोर्ड की आधिकारिक परीक्षा।",
        example: "जैसे अगली कक्षा में जाने के लिए बोर्ड परीक्षा या वार्षिक एग्जाम देना होता है।"
    },
    "further notice": {
        term: "Until Further Notice (अगले आदेश / सूचना तक)",
        simple_meaning: "जब तक विभाग या विश्वविद्यालय द्वारा अगली नई आधिकारिक सूचना जारी नहीं की जाती तब तक",
        contextual_meaning: "वर्तमान निर्णय (जैसे परीक्षा का टलना) तब तक प्रभावी रहेगा जब तक नया आदेश न आ जाए।",
        example: "जैसे 'दुकान अगले आदेश तक बंद रहेगी' — यानी जब तक नई सूचना न आए, दुकान नहीं खुलेगी।"
    },
    "penalty": {
        term: "Penalty (जुर्माना / दंड शुल्क)",
        simple_meaning: "नियम तोड़ने या अंतिम तिथि के बाद काम करने पर लगने वाला अतिरिक्त आर्थिक दंड (Late fee / fine)",
        contextual_meaning: "यदि समय सीमा तक फीस या टैक्स नहीं भरा गया, तो मूल राशि के ऊपर अतिरिक्त जुर्माना लगेगा।",
        example: "जैसे बिना हेलमेट बाइक चलाने पर ट्रैफिक पुलिस चालान (जुर्माना) काटती है।"
    },
    "admit card": {
        term: "Admit Card / Hall Ticket (परीक्षा प्रवेश पत्र)",
        simple_meaning: "परीक्षा हॉल में प्रवेश पाने के लिए आधिकारिक अनुमति पत्र (Exam hall entry ticket)",
        contextual_meaning: "छात्र का रोल नंबर और परीक्षा केंद्र दर्शाने वाला अनिवार्य प्रवेश पत्र जिसके बिना परीक्षा में नहीं बैठ सकते।",
        example: "जैसे सिनेमा हॉल में जाने के लिए मूवी टिकट आवश्यक होता है, वैसे ही एग्जाम में एडमिट कार्ड अनिवार्य है।"
    },
    "arrears": {
        term: "Arrears (पिछला बकाया / देय राशि)",
        simple_meaning: "पिछली तिथियों का वह पैसा या बिल जो समय पर नहीं चुकाया गया और अब बकाया है (Overdue payment)",
        contextual_meaning: "पुराने महीनों या वर्षों का अनपेड टैक्स या फीस जो इस नोटिस में तत्काल मांगी गई है।",
        example: "जैसे पिछले तीन महीनों का बिजली बिल न भरने पर वह 'एरियर्स' (बकाया) के रूप में जुड़कर आता है।"
    },
    "compliance": {
        term: "Compliance (अनुपालन / नियमों का कड़ाई से पालन)",
        simple_meaning: "सरकारी या संस्थागत नियमों और कानूनों के अनुसार कार्य करना (Following the rules)",
        contextual_meaning: "नोटिस में दिए गए निर्देशों और शर्तों को समय सीमा के भीतर पूरा करने की वैधानिक बाध्यता।",
        example: "जैसे सड़क पर लाल बत्ती पर रुकना ट्रैफिक नियमों का अनुपालन (Compliance) है।"
    }
};

// Sample Notices for Instant Demonstration
const SAMPLE_DOCUMENTS = {
    tax: `MUNICIPAL CORPORATION OF GREATER MUMBAI
ASSESSMENT & COLLECTION DEPARTMENT
DEMAND NOTICE UNDER SECTION 202 OF THE MMC ACT

Notice No: MCGM/AC/2026/8942-B
Date of Issue: 15-September-2026
Assessee: M/s Krishna Traders & Property Holdings
Ward: K-West, Andheri West, Mumbai - 400058

SUBJECT: STATUTORY DEMAND FOR OUTSTANDING PROPERTY TAX & DRAINAGE AMENITY CESS

Whereas your registered commercial tenement bearing Property Account No. 89-42-0091-00 is in default of municipal property tax, you are hereby called upon to remit the aggregate statutory dues of ₹42,650/- (Rupees Forty-Two Thousand Six Hundred and Fifty only) within thirty (30) days from the service of this notice.

Failure to remit the aforementioned sum prior to 15-October-2026 shall attract a compulsory penal interest surcharge @ 2% per mensem pursuant to Section 207-A of the MMC Act. 

Furthermore, in the event of persistent non-compliance, distress warrant proceedings shall be initiated without further reference, including the physical attachment and distress of movable property, attachment of bank accounts, or severance of municipal water supply connection.

APPEAL & GRIEVANCE:
If the assessee disputes the rateable value assessed herein, an official statutory objection memorandum may be submitted in Form 'C' to the Deputy Municipal Commissioner (Assessments) at the Ward Office within twenty-one (21) days of receipt, accompanied by proof of pre-deposit of 50% of the disputed demand amount.

By Order of the Municipal Commissioner.`,

    university: `CENTRAL COUNCIL FOR HIGHER EDUCATION & RESEARCH
DIRECTORATE OF ACADEMIC AFFAIRS & EXAMINATIONS
CIRCULAR NO: CCHER/EXAM/REVAL/2026-04

Date: 02 October 2026
To: All Affiliated Constituent Colleges & Deans of Faculties

SUBJECT: MANDATORY DISQUALIFICATION POLICY & SUBMISSION OF END-SEMESTER CONDONATION DOSSIERS

1. ATTENDANCE CONDONATION REGULATIONS:
Pursuant to Ordinance VIII-B, candidate scholars must maintain aggregate biometric attendance of not less than 75% in each stipulated pedagogical module. Candidates possessing attendance between 60% and 74.9% due to substantiated medical incapacity may petition for a Condonation Certificate upon remittance of a non-refundable administrative processing surcharge of ₹1,500/- accompanied by an official affidavit on non-judicial stamp paper.

2. HARD DEADLINE FOR PORTAL ENROLLMENT:
All condonation applications must be endorsed by the Head of Department and electronically uploaded to the Samarth Portal (https://samarth.edu.in/portal/condone) on or before 25-October-2026 (5:00 PM IST). Under no circumstances shall offline physical representations be entertained post the deadline.

3. PENALTY:
Scholars failing to rectify their provisional debarment shall be strictly precluded from obtaining the Admit Card / Hall Ticket for the ensuing Winter Examination Series commencing 10-November-2026. Furthermore, existing merit scholarship disbursements shall be placed in provisional abeyance pending disciplinary audit.

Helpline: academic-support@ccher.ac.in | 011-2389-0091`,

    bank: `RESERVE BANK GUIDELINES COMPLIANCE NOTIFICATION
APEX NATIONAL BANK — FRAUD MONITORING & RISK MITIGATION CELL
NOTICE OF PROVISIONAL INACTIVATION OF UNVERIFIED ACCOUNTS

Reference: ANB/KYC-AUDIT/OCT-2026/7710
Customer ID: 9028471109

Dear Account Holder,

SUBJECT: PERIODIC KYC RE-AUTHENTICATION MANDATE (PREVENTION OF MONEY LAUNDERING ACT)

In compliance with statutory Master Directions issued under the Prevention of Money Laundering Act (PMLA) and Section 35A of the Banking Regulation Act, periodic Updation of Customer Identification Data is mandatory for high-risk and medium-risk savings accounts.

Your account has been flagged for Re-KYC compliance. You are urgently required to furnish the following self-attested documents:
1. Proof of Identity (Aadhaar Card, Passport, or Voter ID).
2. Proof of Address not older than three (3) months.
3. Recent Form 60 or Permanent Account Number (PAN) Card.

DEADLINE & CONSEQUENCES:
The requisite dossier must be presented in person at your home branch or uploaded via our secure banking app before 31-October-2026. 

In default thereof, your account will be placed under 'Debit Freeze' status, precluding UPI transfers, ATM cash withdrawals, and recurring automated standing instructions (NACH/EMIs). No monetary penalties are levied for KYC updation.

For digital verification: https://apexbank.in/kyc-portal | Toll-free: 1800-425-0099.`
};

// Language map for SpeechSynthesis BCP-47 tags
const SPEECH_LANG_MAP = {
    'en': 'en-GB',
    'hi': 'hi-IN',
    'bn': 'bn-IN',
    'te': 'te-IN',
    'mr': 'mr-IN',
    'ta': 'ta-IN',
    'gu': 'gu-IN',
    'kn': 'kn-IN',
    'ml': 'ml-IN',
    'pa': 'pa-IN',
    'or': 'or-IN',
    'as': 'as-IN',
    'ur': 'ur-PK',
    'es': 'es-ES',
    'fr': 'fr-FR',
    'de': 'de-DE'
};

// Initialize Application Lifecycle
document.addEventListener("DOMContentLoaded", () => {
    initEngineHealthCheck();
    initTabs();
    initSampleSelector();
    initDropzonesAndUploads();
    initCameraScanner();
    initAudioControls();
    initWorkflowSubmission();
    initChatWithDocument();
    initResetAndCopy();
    initCustomTermExplainer();
    initExplanationSimplifier();
    initModal();
});

/* ==========================================================================
   1. Backend Connectivity & Operational Health Check
   ========================================================================== */
async function initEngineHealthCheck() {
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    const modalBackendStatus = document.getElementById("modalBackendStatus");

    try {
        const res = await fetch(`${state.backendUrl}/api/health`, { method: "GET" });
        if (res.ok) {
            const data = await res.json();
            state.isBackendOnline = true;
            state.aiProvider = data.provider;
            state.activeModel = data.active_model;

            if (data.ai_engine_configured) {
                statusDot.className = "status-dot green";
                if (data.features?.open_weight_ai) {
                    statusText.innerText = `Vyron Open-Weight AI: Connected (Groq / ${data.active_model})`;
                } else {
                    statusText.innerText = `Vyron Cloud AI: Connected (${data.provider}: ${data.active_model})`;
                }
                if (modalBackendStatus) {
                    modalBackendStatus.innerHTML = `🟢 <strong>Connected to FastAPI Backend</strong><br>Provider: <code>${escapeHtml(data.provider)}</code> | Model: <code>${escapeHtml(data.active_model)}</code><br>Full Open-Weight Generative AI reasoning & Grounded Q&A Active.`;
                }
            } else {
                statusDot.className = "status-dot yellow";
                statusText.innerText = "Vyron Hybrid Mode: Connected (Direct Translation & Regex Extraction Active)";
                if (modalBackendStatus) {
                    modalBackendStatus.innerHTML = `🟡 <strong>Backend Connected in Hybrid Mode</strong><br>Multilingual translation active without cloud credentials.<br>To enable full LLM reasoning, configure <code>GROQ_API_KEY</code> in <code>.env</code>.`;
                }
            }
            return;
        }
    } catch (e) {
        // Backend not reachable
    }

    state.isBackendOnline = false;
    statusDot.className = "status-dot yellow";
    statusText.innerText = "Vyron Standalone Mode: Direct Translation & In-Browser OCR Active";
    if (modalBackendStatus) {
        modalBackendStatus.innerHTML = `⚪ <strong>Standalone Client Mode Active</strong><br>Running client-side PDF.js, Tesseract.js OCR, and direct translation directly in your browser.`;
    }
}

/* ==========================================================================
   2. Input Tabs Navigation
   ========================================================================== */
function initTabs() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => {
                b.classList.remove("active");
                b.setAttribute("aria-selected", "false");
            });
            btn.classList.add("active");
            btn.setAttribute("aria-selected", "true");

            const targetPaneId = btn.getAttribute("data-tab");
            state.currentTab = targetPaneId;

            document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
            const targetPane = document.getElementById(targetPaneId);
            if (targetPane) targetPane.classList.add("active");

            // Stop camera if user navigated away from camera tab
            if (targetPaneId !== "paneCamera") {
                stopCamera();
            }
        });
    });

    // Character counter for textarea
    const sourceText = document.getElementById("sourceText");
    const charCount = document.getElementById("charCount");
    sourceText.addEventListener("input", () => {
        charCount.innerText = `${sourceText.value.length} characters`;
    });

    document.getElementById("clearTextBtn").addEventListener("click", () => {
        sourceText.value = "";
        charCount.innerText = "0 characters";
    });
}

/* ==========================================================================
   3. Sample Notice Selector (Instant Demo Acceleration)
   ========================================================================== */
function initSampleSelector() {
    const sampleSelect = document.getElementById("sampleDocSelect");
    sampleSelect.addEventListener("change", (e) => {
        const key = e.target.value;
        if (!key || !SAMPLE_DOCUMENTS[key]) return;

        // Switch to direct text tab
        document.getElementById("tabText").click();
        const textarea = document.getElementById("sourceText");
        textarea.value = SAMPLE_DOCUMENTS[key];
        document.getElementById("charCount").innerText = `${textarea.value.length} characters`;

        // Highlight input card momentarily
        const inputCard = document.querySelector(".input-card");
        inputCard.style.boxShadow = "0 0 35px var(--primary-glow)";
        setTimeout(() => inputCard.style.boxShadow = "", 800);
    });
}

/* ==========================================================================
   4. Ingestion: PDF (Drag & Drop + PDF.js Client Preview)
   ========================================================================== */
function initDropzonesAndUploads() {
    // PDF Handling
    const pdfDropzone = document.getElementById("pdfDropzone");
    const pdfInput = document.getElementById("pdfFileInput");
    const pdfPreviewCard = document.getElementById("pdfPreviewCard");
    const pdfFileName = document.getElementById("pdfFileName");
    const pdfFileMeta = document.getElementById("pdfFileMeta");
    const pdfExtractedBox = document.getElementById("pdfExtractedBox");
    const pdfExtractedText = document.getElementById("pdfExtractedText");

    pdfDropzone.addEventListener("click", () => pdfInput.click());
    pdfDropzone.addEventListener("dragover", (e) => { e.preventDefault(); pdfDropzone.classList.add("dragover"); });
    pdfDropzone.addEventListener("dragleave", () => pdfDropzone.classList.remove("dragover"));
    pdfDropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        pdfDropzone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handlePdfFile(e.dataTransfer.files[0]);
        }
    });

    pdfInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handlePdfFile(e.target.files[0]);
        }
    });

    document.getElementById("removePdfBtn").addEventListener("click", () => {
        state.selectedFile = null;
        state.extractedSourceText = "";
        pdfInput.value = "";
        pdfPreviewCard.style.display = "none";
        pdfExtractedBox.style.display = "none";
        pdfExtractedText.value = "";
        pdfDropzone.style.display = "block";
    });

    async function handlePdfFile(file) {
        if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
            showError("Invalid File Format", "Please upload a valid PDF document.");
            return;
        }
        if (file.size > 15 * 1024 * 1024) {
            showError("File Too Large", "PDF exceeds maximum allowed limit of 15MB.");
            return;
        }

        state.selectedFile = file;
        pdfDropzone.style.display = "none";
        pdfPreviewCard.style.display = "flex";
        pdfFileName.innerText = file.name;
        pdfFileMeta.innerText = `Parsing pages... | ${(file.size / 1024).toFixed(1)} KB`;

        try {
            if (window.pdfjsLib) {
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                const arrayBuffer = await file.arrayBuffer();
                const pdfDoc = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
                const numPages = pdfDoc.numPages;
                pdfFileMeta.innerText = `${numPages} Page(s) | ${(file.size / 1024).toFixed(1)} KB`;

                let extracted = "";
                const maxPages = Math.min(numPages, 10);
                for (let i = 1; i <= maxPages; i++) {
                    const page = await pdfDoc.getPage(i);
                    const textContent = await page.getTextContent();
                    const pageText = textContent.items.map(item => item.str).join(' ');
                    extracted += `--- Page ${i} ---\n${pageText}\n\n`;
                }
                const cleanExtracted = extracted.trim();
                state.extractedSourceText = cleanExtracted;
                pdfExtractedText.value = cleanExtracted;
                pdfExtractedBox.style.display = "block";
            }
        } catch (e) {
            pdfFileMeta.innerText = `PDF ready for server extraction | ${(file.size / 1024).toFixed(1)} KB`;
        }
    }

    // Image Handling
    const imageDropzone = document.getElementById("imageDropzone");
    const imageInput = document.getElementById("imageFileInput");
    const imagePreviewContainer = document.getElementById("imagePreviewContainer");
    const imagePreview = document.getElementById("imagePreview");
    const imageMetaText = document.getElementById("imageMetaText");
    const runImageOcrBtn = document.getElementById("runImageOcrBtn");
    const imageOcrStatusBadge = document.getElementById("imageOcrStatusBadge");
    const imageOcrEditWrap = document.getElementById("imageOcrEditWrap");
    const imageExtractedText = document.getElementById("imageExtractedText");

    imageDropzone.addEventListener("click", () => imageInput.click());
    imageDropzone.addEventListener("dragover", (e) => { e.preventDefault(); imageDropzone.classList.add("dragover"); });
    imageDropzone.addEventListener("dragleave", () => imageDropzone.classList.remove("dragover"));
    imageDropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        imageDropzone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleImageFile(e.dataTransfer.files[0]);
        }
    });

    imageInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleImageFile(e.target.files[0]);
        }
    });

    document.getElementById("removeImageBtn").addEventListener("click", () => {
        state.selectedFile = null;
        imageInput.value = "";
        imagePreviewContainer.style.display = "none";
        imageDropzone.style.display = "block";
        imageExtractedText.value = "";
        imageOcrEditWrap.style.display = "none";
        imageOcrStatusBadge.innerText = "Ready for OCR";
        imageOcrStatusBadge.className = "badge";
    });

    function handleImageFile(file) {
        const allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/webp"];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(jpe?g|png|webp)$/i)) {
            showError("Invalid File Format", "Please upload a JPG, PNG, or WEBP image.");
            return;
        }

        state.selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imageDropzone.style.display = "none";
            imagePreviewContainer.style.display = "block";
            imageMetaText.innerText = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
            imageOcrStatusBadge.innerText = "Image Loaded — Ready for OCR";
            imageOcrStatusBadge.className = "badge";
            
            // Auto trigger OCR on load for high responsiveness
            triggerImageOcr();
        };
        reader.readAsDataURL(file);
    }

    runImageOcrBtn.addEventListener("click", () => triggerImageOcr());

    async function triggerImageOcr() {
        if (!imagePreview.src) return;
        runImageOcrBtn.disabled = true;
        imageOcrStatusBadge.innerText = "Processing OCR...";
        imageOcrStatusBadge.className = "badge badge-accent";

        try {
            const extracted = await runClientSideOcr(imagePreview.src);
            imageExtractedText.value = extracted;
            imageOcrEditWrap.style.display = "block";
            imageOcrStatusBadge.innerText = "✅ OCR Extraction Complete";
            imageOcrStatusBadge.className = "badge";
            state.extractedSourceText = extracted;
        } catch (err) {
            imageOcrStatusBadge.innerText = "OCR Failed";
            imageOcrStatusBadge.className = "badge badge-danger";
            showError("OCR Notice", err.message || "Unable to recognize readable text. Please check image sharpness or enter text manually.");
            imageOcrEditWrap.style.display = "block";
        } finally {
            runImageOcrBtn.disabled = false;
        }
    }
}

/* ==========================================================================
   5. Live WebRTC Camera Scanner (Flip, Capture, Retake, OCR)
   ========================================================================== */
function initCameraScanner() {
    const startBtn = document.getElementById("startCameraBtn");
    const container = document.getElementById("cameraContainer");
    const placeholder = document.getElementById("cameraPlaceholder");
    const video = document.getElementById("cameraFeed");
    const canvas = document.getElementById("cameraCanvas");
    const snapshotImg = document.getElementById("cameraSnapshotPreview");
    const liveControls = document.getElementById("cameraLiveControls");
    const reviewControls = document.getElementById("cameraReviewControls");
    const switchBtn = document.getElementById("switchCameraBtn");
    const captureBtn = document.getElementById("captureBtn");
    const retakeBtn = document.getElementById("retakeCameraBtn");
    const usePhotoBtn = document.getElementById("useCameraPhotoBtn");
    const cancelBtn = document.getElementById("cancelCameraBtn");
    const cameraOcrEditWrap = document.getElementById("cameraOcrEditWrap");
    const cameraExtractedText = document.getElementById("cameraExtractedText");

    // Native OS Device Camera Bridge (100% immune to WebRTC browser permission locks)
    const nativeBtn = document.getElementById("nativeCameraBtn");
    const nativeInput = document.getElementById("nativeCameraInput");
    if (nativeBtn && nativeInput) {
        nativeBtn.addEventListener("click", () => nativeInput.click());
        nativeInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                state.selectedFile = file;
                const reader = new FileReader();
                reader.onload = async (ev) => {
                    snapshotImg.src = ev.target.result;
                    snapshotImg.style.display = "block";
                    video.style.display = "none";
                    placeholder.style.display = "none";
                    container.style.display = "block";
                    liveControls.style.display = "none";
                    reviewControls.style.display = "flex";

                    try {
                        const extracted = await runClientSideOcr(ev.target.result);
                        cameraExtractedText.value = extracted;
                        cameraOcrEditWrap.style.display = "block";
                        state.extractedSourceText = extracted;
                    } catch (err) {
                        showError("OCR Notice", err.message || "Could not read text. Please enter text manually.");
                        cameraOcrEditWrap.style.display = "block";
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    startBtn.addEventListener("click", async () => {
        await startCamera();
    });

    switchBtn.addEventListener("click", async () => {
        state.cameraFacingMode = (state.cameraFacingMode === "environment") ? "user" : "environment";
        await startCamera();
    });

    cancelBtn.addEventListener("click", () => {
        stopCamera();
    });

    async function startCamera() {
        if (!navigator.mediaDevices?.getUserMedia) {
            showError("Camera Unavailable", "Your browser does not support WebRTC camera access. Please use Option B (Direct Device Camera).");
            return;
        }

        stopCameraTracks();

        try {
            // Progressive constraint candidates to prevent overconstrained or locked camera errors
            const constraintOptions = [
                { video: { facingMode: { ideal: state.cameraFacingMode } }, audio: false },
                { video: { facingMode: state.cameraFacingMode }, audio: false },
                { video: true, audio: false }
            ];

            let stream = null;
            let lastErr = null;
            for (const c of constraintOptions) {
                try {
                    stream = await navigator.mediaDevices.getUserMedia(c);
                    if (stream) break;
                } catch (err) {
                    lastErr = err;
                }
            }

            if (!stream) {
                throw lastErr || new Error("Could not initialize camera stream.");
            }

            state.cameraStream = stream;
            video.srcObject = stream;
            video.muted = true;
            await video.play();

            video.style.display = "block";
            snapshotImg.style.display = "none";
            placeholder.style.display = "none";
            container.style.display = "block";
            liveControls.style.display = "flex";
            reviewControls.style.display = "none";
        } catch (e) {
            stopCamera();
            const explanations = {
                NotAllowedError: "Camera permission was blocked. Click the lock 🔒 icon next to your URL in the address bar, toggle Camera to 'Allow', and refresh. Or use Option B (Direct Device Camera).",
                NotFoundError: "No camera sensor was detected. You can use Option B or upload an image.",
                NotReadableError: "Camera is currently locked by another program (Windows Camera, Zoom, Teams, or another browser tab). Please close other camera apps."
            };
            showError("Camera Notice", explanations[e.name] || `Could not open camera stream: ${e.message}`);
        }
    }

    captureBtn.addEventListener("click", () => {
        if (!state.cameraStream || !video.videoWidth || !video.videoHeight) {
            showError("Camera Not Ready", "Please wait for the live preview to initialize before capturing.");
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataUrl = canvas.toDataURL("image/jpeg", 0.95);
        snapshotImg.src = dataUrl;

        // Switch to review mode
        video.style.display = "none";
        snapshotImg.style.display = "block";
        liveControls.style.display = "none";
        reviewControls.style.display = "flex";
    });

    retakeBtn.addEventListener("click", () => {
        snapshotImg.style.display = "none";
        snapshotImg.src = "";
        if (state.cameraStream) {
            video.style.display = "block";
            liveControls.style.display = "flex";
            reviewControls.style.display = "none";
        } else {
            // Re-show choice placeholder if camera was closed
            container.style.display = "none";
            placeholder.style.display = "block";
        }
    });

    usePhotoBtn.addEventListener("click", async () => {
        usePhotoBtn.disabled = true;
        usePhotoBtn.innerText = "Processing OCR...";

        const processSource = snapshotImg.src || (canvas.width > 0 ? canvas.toDataURL("image/jpeg", 0.95) : null);
        if (!processSource) {
            showError("No Photo", "Please capture or select a photo first.");
            usePhotoBtn.disabled = false;
            usePhotoBtn.innerText = "⚡ Use Photo & Run OCR";
            return;
        }

        try {
            const extracted = await runClientSideOcr(processSource);
            cameraExtractedText.value = extracted;
            cameraOcrEditWrap.style.display = "block";
            state.extractedSourceText = extracted;
            stopCamera();
        } catch (err) {
            showError("OCR Notice", err.message || "Unable to recognize text in captured photo. Try capturing under better lighting.");
            cameraOcrEditWrap.style.display = "block";
        } finally {
            usePhotoBtn.disabled = false;
            usePhotoBtn.innerText = "⚡ Use Photo & Run OCR";
        }
    });

    window.addEventListener("pagehide", stopCamera);
}

function stopCameraTracks() {
    if (state.cameraStream) {
        state.cameraStream.getTracks().forEach(t => t.stop());
        state.cameraStream = null;
    }
}

function stopCamera() {
    stopCameraTracks();
    const container = document.getElementById("cameraContainer");
    const placeholder = document.getElementById("cameraPlaceholder");
    const video = document.getElementById("cameraFeed");
    if (video) video.srcObject = null;
    if (container) container.style.display = "none";
    if (placeholder) placeholder.style.display = "block";
}

/* ==========================================================================
   6. Optical Character Recognition (Tesseract.js Engine with Preprocessing)
   ========================================================================== */
async function runClientSideOcr(imageSource) {
    const pane = document.getElementById("ocrProgressContainer");
    const bar = document.getElementById("ocrProgressBar");
    const label = document.getElementById("ocrStatusLabel");

    pane.style.display = "block";
    bar.style.width = "15%";
    label.innerText = "Initializing OCR language models (English + Hindi)...";

    // Image preprocessing via offscreen canvas for improved contrast
    let processedSource = imageSource;
    try {
        const img = new Image();
        img.crossOrigin = "anonymous";
        await new Promise((resolve, reject) => {
            img.onload = resolve;
            img.onerror = reject;
            img.src = imageSource;
        });

        const offCanvas = document.createElement("canvas");
        offCanvas.width = img.naturalWidth || img.width;
        offCanvas.height = img.naturalHeight || img.height;
        const ctx = offCanvas.getContext("2d");
        ctx.drawImage(img, 0, 0);

        // Simple contrast & threshold boost
        const imgData = ctx.getImageData(0, 0, offCanvas.width, offCanvas.height);
        const data = imgData.data;
        for (let i = 0; i < data.length; i += 4) {
            const gray = (0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
            // Subtle high-pass contrast curve
            const boosted = gray > 140 ? Math.min(255, gray * 1.15) : Math.max(0, gray * 0.85);
            data[i] = boosted;
            data[i + 1] = boosted;
            data[i + 2] = boosted;
        }
        ctx.putImageData(imgData, 0, 0);
        processedSource = offCanvas.toDataURL("image/jpeg", 0.92);
    } catch (e) {
        processedSource = imageSource;
    }

    let worker = null;
    try {
        if (!window.Tesseract) {
            throw new Error("OCR library could not be loaded. Please check your internet connection.");
        }

        label.innerText = "Loading Tesseract OCR worker (eng + hin)...";
        bar.style.width = "35%";

        worker = await Tesseract.createWorker("eng+hin", 1, {
            logger: (m) => {
                if (m.status === "recognizing text") {
                    const pct = Math.round((m.progress || 0) * 50) + 45;
                    bar.style.width = `${pct}%`;
                    label.innerText = `Recognizing text... ${Math.round((m.progress || 0) * 100)}%`;
                }
            }
        });

        label.innerText = "Analyzing characters and language syntax...";
        const ret = await worker.recognize(processedSource);
        const text = (ret.data?.text || "").trim();

        if (text.length < 5) {
            throw new Error("Unable to recognize readable text. Please upload a clearer image or enter the text manually.");
        }

        bar.style.width = "100%";
        return text;
    } finally {
        if (worker) {
            await worker.terminate().catch(() => {});
        }
        setTimeout(() => {
            pane.style.display = "none";
        }, 500);
    }
}

/* ==========================================================================
   7. Main Workflow Processing & Submission Pipeline
   ========================================================================== */
function initWorkflowSubmission() {
    const translateBtn = document.getElementById("translateBtn");
    const aiCore = document.getElementById("aiCore");
    const pipeline = document.getElementById("processingPipeline");
    const resultsWrapper = document.getElementById("resultsWrapper");

    translateBtn.addEventListener("click", async () => {
        hideError();
        let textToProcess = "";

        // Collect text based on the active tab
        if (state.currentTab === "paneText") {
            textToProcess = document.getElementById("sourceText").value.trim();
        } else if (state.currentTab === "panePdf") {
            const pdfExt = document.getElementById("pdfExtractedText").value.trim();
            textToProcess = pdfExt || state.extractedSourceText;
        } else if (state.currentTab === "paneImage") {
            const imgExt = document.getElementById("imageExtractedText").value.trim();
            textToProcess = imgExt || state.extractedSourceText;
        } else if (state.currentTab === "paneCamera") {
            const camExt = document.getElementById("cameraExtractedText").value.trim();
            textToProcess = camExt || state.extractedSourceText;
        }

        if (!textToProcess && !state.selectedFile) {
            showError("No Document Provided", "Please enter text, upload a PDF/Image, or scan a document with your camera.");
            return;
        }

        const targetLang = document.getElementById("targetLang").value;
        const level = document.querySelector('input[name="explanationLevel"]:checked').value;

        // Visual Pipeline Activation
        aiCore.classList.add("processing");
        pipeline.style.display = "block";
        resultsWrapper.style.display = "none";
        translateBtn.disabled = true;
        translateBtn.style.opacity = "0.7";

        updatePipelineStep(1, "Extracting text and verifying structure...");

        try {
            let resultData = null;

            if (state.isBackendOnline) {
                updatePipelineStep(2, "Translating document content faithfully...");
                const formData = new FormData();
                if (textToProcess) {
                    formData.append("text", textToProcess);
                } else if (state.selectedFile) {
                    formData.append("file", state.selectedFile);
                }
                formData.append("target_lang", targetLang);
                formData.append("explanation_level", level);

                const response = await fetch(`${state.backendUrl}/api/process-document`, {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    const errJson = await response.json().catch(() => ({}));
                    throw new Error(errJson.detail || `Server returned error status ${response.status}`);
                }

                updatePipelineStep(3, "Synthesizing simplified civic explanation...");
                await new Promise(r => setTimeout(r, 350));
                updatePipelineStep(4, "Decoding official jargon & extracting deadlines...");
                await new Promise(r => setTimeout(r, 250));

                resultData = await response.json();
            } else {
                // Standalone Client-Side Execution
                updatePipelineStep(2, "Translating text chunk by chunk...");
                const translated = await clientTranslate(textToProcess, targetLang);

                updatePipelineStep(3, "Synthesizing simplified civic explanation...");
                await new Promise(r => setTimeout(r, 350));

                updatePipelineStep(4, "Decoding official jargon & identifying actions...");
                await new Promise(r => setTimeout(r, 250));

                const analysis = await clientHeuristicAnalysis(textToProcess, translated.text, targetLang, level);
                resultData = {
                    status: "success",
                    metadata: { source: "client_standalone" },
                    original_text: textToProcess,
                    literal_translated_text: translated.text,
                    faithful_translation: translated.text,
                    target_lang: targetLang,
                    analysis: analysis
                };
            }

            state.lastAnalysisData = resultData;
            state.extractedSourceText = resultData.original_text || textToProcess;

            // Render complete 6-tab dashboard
            renderResultsDashboard(resultData);

            pipeline.style.display = "none";
            resultsWrapper.style.display = "flex";
            resultsWrapper.scrollIntoView({ behavior: "smooth", block: "start" });

        } catch (err) {
            showError("Processing Error", err.message || "Failed to process document.");
            pipeline.style.display = "none";
        } finally {
            aiCore.classList.remove("processing");
            translateBtn.disabled = false;
            translateBtn.style.opacity = "1";
        }
    });

    // 6-Tab Result View Switcher
    const resTabs = document.querySelectorAll(".res-tab");
    resTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            resTabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const targetViewId = tab.getAttribute("data-view");
            document.querySelectorAll(".result-view-panel").forEach(p => p.classList.remove("active"));
            const targetPanel = document.getElementById(targetViewId);
            if (targetPanel) targetPanel.classList.add("active");
        });
    });
}

function updatePipelineStep(stepNum, statusText) {
    document.getElementById("pipelineStatusText").innerText = statusText;
    for (let i = 1; i <= 4; i++) {
        const node = document.getElementById(`step${i}`);
        const line = document.getElementById(`line${i}`);
        if (i <= stepNum) {
            node.classList.add("active");
            if (line) line.classList.add("active");
        } else {
            node.classList.remove("active");
            if (line) line.classList.remove("active");
        }
    }
}

/* ==========================================================================
   8. Client-Side Chunked Translation & Heuristic Analysis
   ========================================================================== */
async function clientTranslate(text, targetLang) {
    if (!text || !text.trim()) return { text: "" };

    // 1. Primary: Use FastAPI Backend if reachable (uses robust dictionary translation engine)
    if (state.isBackendOnline) {
        try {
            const res = await fetch(`${state.backendUrl}/api/translate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text, target_lang: targetLang })
            });
            if (res.ok) {
                const data = await res.json();
                if (data.translated_text) {
                    return { text: data.translated_text };
                }
            }
        } catch (e) {}
    }

    // 2. Secondary: Google Dictionary Endpoint (No 429 block)
    try {
        const urlDict = `https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=${targetLang}&q=${encodeURIComponent(text.slice(0, 1000))}`;
        const resDict = await fetch(urlDict);
        if (resDict.ok) {
            const jsonDict = await resDict.json();
            if (Array.isArray(jsonDict) && jsonDict.length > 0) {
                const first = jsonDict[0];
                if (typeof first === "string" && first.trim()) return { text: first.trim() };
                if (Array.isArray(first) && first.length > 0 && typeof first[0] === "string") return { text: first[0].trim() };
            }
        }
    } catch (e) {}

    // 3. Tertiary: Google Public Translate via GTX
    try {
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLang}&dt=t&q=${encodeURIComponent(text.slice(0, 1000))}`;
        const res = await fetch(url);
        if (res.ok) {
            const json = await res.json();
            if (json && json[0]) {
                const tr = json[0].map(s => s[0]).join('');
                if (tr.trim()) return { text: tr };
            }
        }
    } catch (e) {}

    // 4. Quaternary: MyMemory (filtering out corrupted crowdsourced strings)
    try {
        const url2 = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text.slice(0, 450))}&langpair=autodetect|${targetLang}`;
        const res2 = await fetch(url2);
        if (res2.ok) {
            const json2 = await res2.json();
            const t = json2.responseData?.translatedText;
            if (t && !t.startsWith("MYMEMORY WARNING") && t !== "gdhgd" && !t.includes("PLEASE SELECT")) return { text: t };
        }
    } catch (e) {}

    return { text: text };
}

async function clientHeuristicAnalysis(rawText, translatedBody, targetLang, level) {
    const dateMatches = rawText.match(/\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}|\d+\s+days?)\b/gi);
    const deadlineRaw = dateMatches ? Array.from(new Set(dateMatches)).slice(0, 3).join(", ") : "";

    const feeMatches = rawText.match(/(?:Rs\.?|INR|₹|\$)\s*[\d,]+(?:\.\d{2})?/gi);
    const feesRaw = feeMatches ? Array.from(new Set(feeMatches)).slice(0, 3).join(", ") : "";

    const notSpecified = targetLang === "en" ? "Not specified in document" : (await clientTranslate("Not specified in document", targetLang)).text;
    const deadlineVal = deadlineRaw ? (await clientTranslate(`Deadline: ${deadlineRaw}`, targetLang)).text : notSpecified;
    const feeVal = feesRaw ? (await clientTranslate(`Fees / Amount: ${feesRaw}`, targetLang)).text : notSpecified;

    const action1 = (await clientTranslate("Carefully review the obligations and directives stated above.", targetLang)).text;
    const action2 = (await clientTranslate("Submit all required forms or payments before the deadline.", targetLang)).text;
    const takeaway1 = (await clientTranslate("Official notice translated and simplified for citizen comprehension.", targetLang)).text;
    const takeaway2 = (await clientTranslate(`Important deadlines detected: ${deadlineRaw || 'None specified'}`, targetLang)).text;
    const warning = (await clientTranslate("Please cross-reference all penalty clauses and dates against the original document.", targetLang)).text;
    const docs = (await clientTranslate("Identification or official papers as cited in original text.", targetLang)).text;
    const penalties = (await clientTranslate("Administrative penalties or surcharges may apply if ignored.", targetLang)).text;
    const docType = (await clientTranslate("Government Notice / Circular", targetLang)).text;

    // Extract authoritative known jargon terms from Civic Knowledge Base
    const jargonList = [];
    const textLower = rawText.toLowerCase();

    for (const [key, item] of Object.entries(CIVIC_CLIENT_DICTIONARY)) {
        if (textLower.includes(key)) {
            const sentenceMatch = rawText.match(new RegExp(`([^.?!।\\n]*\\b${key}\\b[^.?!।\\n]*[.?!।])`, 'i'));
            const sent = sentenceMatch ? sentenceMatch[1].trim() : `Mentioned in notice: '${key}'.`;
            const meaning = targetLang === 'hi' ? item.simple_meaning : (await clientTranslate(item.simple_meaning, targetLang)).text;
            const ctx = targetLang === 'hi' ? item.contextual_meaning : (await clientTranslate(item.contextual_meaning, targetLang)).text;
            const ex = targetLang === 'hi' ? item.example : (await clientTranslate(item.example, targetLang)).text;

            jargonList.push({
                term: item.term,
                simple_meaning: meaning,
                contextual_meaning: ctx,
                example: ex,
                source_sentence: sent
            });
            if (jargonList.length >= 4) break;
        }
    }

    // If fewer than 3 terms found, supplement from long words
    if (jargonList.length < 3) {
        const words = rawText.match(/\b[A-Za-z]{8,}\b/g) || [];
        const uniqueWords = Array.from(new Set(words)).slice(0, 3);
        for (const w of uniqueWords) {
            if (jargonList.some(j => j.term.toLowerCase().includes(w.toLowerCase()))) continue;
            const sentenceMatch = rawText.match(new RegExp(`([^.?!]*\\b${w}\\b[^.?!]*[.?!])`, 'i'));
            const sent = sentenceMatch ? sentenceMatch[1].trim() : `Contains term '${w}'.`;
            const meaning = (await clientTranslate(w, targetLang)).text;
            const ctx = (await clientTranslate(`Statutory term appearing in notice: '${meaning}'`, targetLang)).text;
            const ex = (await clientTranslate("Official legal terminology requiring compliance.", targetLang)).text;

            jargonList.push({
                term: w,
                simple_meaning: meaning,
                contextual_meaning: ctx,
                example: ex,
                source_sentence: sent
            });
            if (jargonList.length >= 4) break;
        }
    }

    return {
        ai_engine_active: false,
        engine_note: "Client Hybrid Mode: Real translation active without cloud credentials.",
        detected_source_language: "Auto-Detected",
        document_type: docType,
        simple_explanation: {
            overall_purpose: translatedBody.slice(0, 260) + (translatedBody.length > 260 ? "..." : ""),
            level: level,
            simplified_body: translatedBody,
            key_takeaways: [takeaway1, takeaway2],
            ambiguities_or_warnings: warning
        },
        what_you_need_to_do: {
            required_actions: [action1, action2],
            deadlines: deadlineVal,
            fees_and_payments: feeVal,
            required_documents: [docs],
            eligibility_conditions: notSpecified,
            contact_and_links: notSpecified,
            penalties_or_consequences: penalties
        },
        jargon_decoded: jargonList
    };
}

/* ==========================================================================
   9. Results Dashboard Rendering (Across 6 Tabs)
   ========================================================================== */
function renderResultsDashboard(data) {
    const analysis = data.analysis;
    const simple = analysis.simple_explanation || {};
    const actions = analysis.what_you_need_to_do || {};
    const jargon = analysis.jargon_decoded || [];

    // Tab 1: Overview & Simple Meaning
    document.getElementById("documentTypeBadge").innerText = analysis.document_type || "Official Document";
    document.getElementById("simpleOverallPurpose").innerText = simple.overall_purpose || "No overall purpose summary available.";

    const bodyContainer = document.getElementById("simpleExplanationBody");
    bodyContainer.innerHTML = "";
    const paragraphs = (simple.simplified_body || "").split("\n\n");
    paragraphs.forEach(pText => {
        if (pText.trim()) {
            const p = document.createElement("p");
            p.innerText = pText.trim();
            bodyContainer.appendChild(p);
        }
    });

    const takeawaysBox = document.getElementById("takeawaysBox");
    const takeawaysList = document.getElementById("takeawaysList");
    if (simple.key_takeaways && simple.key_takeaways.length > 0) {
        takeawaysBox.style.display = "block";
        takeawaysList.innerHTML = simple.key_takeaways.map(t => `<li>${escapeHtml(t)}</li>`).join("");
    } else {
        takeawaysBox.style.display = "none";
    }

    const ambiguitiesBox = document.getElementById("ambiguitiesBox");
    const ambiguitiesText = document.getElementById("ambiguitiesText");
    if (simple.ambiguities_or_warnings) {
        ambiguitiesBox.style.display = "flex";
        ambiguitiesText.innerText = simple.ambiguities_or_warnings;
    } else {
        ambiguitiesBox.style.display = "none";
    }

    // Tab 2: Full Faithful Translation
    const literalBox = document.getElementById("literalTranslationBox");
    literalBox.innerText = data.faithful_translation || data.literal_translated_text || "Translation not available.";

    // Tab 3: Jargon Decoded
    const jargonGrid = document.getElementById("jargonCardsContainer");
    jargonGrid.innerHTML = "";
    if (jargon.length === 0) {
        jargonGrid.innerHTML = `<div class="jargon-card"><div class="jargon-context">No complex bureaucratic jargon detected in this document.</div></div>`;
    } else {
        jargon.forEach(item => {
            const card = document.createElement("div");
            card.className = "jargon-card";
            card.innerHTML = `
                <div class="jargon-card-top">
                    <span class="jargon-term">${escapeHtml(item.term)}</span>
                    <button class="icon-btn speak-term-btn" type="button" data-term="${escapeHtml(item.term)}" data-meaning="${escapeHtml(item.simple_meaning)}">
                        🔊 Read
                    </button>
                </div>
                <div class="jargon-meaning">👉 ${escapeHtml(item.simple_meaning)}</div>
                <div class="jargon-context"><strong>Context:</strong> ${escapeHtml(item.contextual_meaning)}</div>
                ${item.example ? `<div class="jargon-example"><strong>Example:</strong> ${escapeHtml(item.example)}</div>` : ''}
                ${item.source_sentence ? `<div class="jargon-source">"${escapeHtml(item.source_sentence)}"</div>` : ''}
            `;
            jargonGrid.appendChild(card);
        });

        jargonGrid.querySelectorAll(".speak-term-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const term = btn.getAttribute("data-term");
                const meaning = btn.getAttribute("data-meaning");
                speakText(`${term}. ${meaning}`, data.target_lang);
            });
        });
    }

    // Tab 4: Action Points
    const actionChecklist = document.getElementById("actionChecklist");
    actionChecklist.innerHTML = "";
    const requiredActions = actions.required_actions || ["Review document instructions."];
    requiredActions.forEach((act, idx) => {
        const item = document.createElement("label");
        item.className = "action-check-item";
        item.innerHTML = `
            <input type="checkbox" id="actionCheck_${idx}">
            <span>${escapeHtml(act)}</span>
        `;
        actionChecklist.appendChild(item);
    });

    document.getElementById("actionDeadline").innerText = actions.deadlines || "Not specified in document";
    document.getElementById("actionFees").innerText = actions.fees_and_payments || "Not specified in document";
    const docVal = Array.isArray(actions.required_documents) ? actions.required_documents.join(", ") : (actions.required_documents || "Not specified in document");
    document.getElementById("actionDocuments").innerText = docVal;
    document.getElementById("actionPenalties").innerText = actions.penalties_or_consequences || "Not specified in document";
    document.getElementById("actionEligibility").innerText = actions.eligibility_conditions || "Not specified in document";
    document.getElementById("actionContact").innerText = actions.contact_and_links || "Not specified in document";

    // Tab 6: Original Source Text
    document.getElementById("rawSourceTextBox").innerText = data.original_text || "Source text not available.";
}

function extractTargetWordClient(question) {
    const q = question.trim().toLowerCase();
    const m_does = q.match(/what\s+does\s+['"]?([a-z\s]{2,40}?)['"]?\s+mean/i);
    if (m_does) return m_does[1].trim();

    const m = q.match(/(?:what\s+is\s+(?:the\s+)?meaning\s+of|meaning\s+of|define|explain\s+word|word\s+meaning)\s*['":]?\s*([a-z\s]{2,40})['":]?/i);
    if (m) {
        let w = m[1].trim().replace(/[?.!,]+$/, '').trim();
        w = w.replace(/\b(in hindi|in english|in document|means|mean)\b/gi, '').trim();
        if (w) return w;
    }

    const m_hi = q.match(/^['"]?([a-z\s]{2,30}?)['"]?\s+(?:ka\s+matlab|ka\s+arth|kya\s+hai|kya\s+hota\s+hai)/i);
    if (m_hi) return m_hi[1].trim();

    const m2 = q.match(/^['"]?([a-z\s]{2,30}?)['"]?\s+(?:meaning|means)\b/i);
    if (m2) return m2[1].trim();

    const words = q.match(/[a-z]+/gi) || [];
    const stopwords = new Set(["what", "who", "when", "where", "how", "why", "which", "is", "are", "the", "this", "that", "can", "could", "should", "tell", "show", "help"]);
    if (words.length >= 1 && words.length <= 2 && !words.some(w => stopwords.has(w))) {
        return words.join(" ");
    }
    return null;
}

/* ==========================================================================
   10. Feature 3: Chat With Your Document ("Ask Vyron Anything")
   ========================================================================== */
function initChatWithDocument() {
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const chatHistory = document.getElementById("chatHistoryContainer");
    const chips = document.querySelectorAll(".chat-chip");

    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            const question = chip.getAttribute("data-q");
            if (question) {
                chatInput.value = question;
                submitChatQuestion(question);
            }
        });
    });

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const q = chatInput.value.trim();
        if (q) {
            submitChatQuestion(q);
        }
    });

    async function submitChatQuestion(question) {
        const docText = state.extractedSourceText || document.getElementById("rawSourceTextBox").innerText;
        if (!docText.trim()) {
            showError("Document Missing", "Please ingest a document first before asking questions.");
            return;
        }

        const targetLang = document.getElementById("targetLang").value;

        // Render user message in chat
        appendChatMessage("user", "You", question);
        chatInput.value = "";

        // Placeholder AI thinking message
        const thinkingId = appendChatMessage("ai", "🤖 Vyron Assistant", "Searching document passages...");

        try {
            let answerData = null;

            if (state.isBackendOnline) {
                const res = await fetch(`${state.backendUrl}/api/chat-document`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        document_text: docText,
                        question: question,
                        target_lang: targetLang
                    })
                });

                if (!res.ok) {
                    throw new Error(`Server returned error status ${res.status}`);
                }
                answerData = await res.json();
            } else {
                // Client-side grounded search fallback
                const targetWord = extractTargetWordClient(question);
                const sentences = docText.split(/[.!?।\n]+/);

                if (targetWord) {
                    const tLower = targetWord.toLowerCase();
                    let matchedKb = null;
                    for (const [k, v] of Object.entries(CIVIC_CLIENT_DICTIONARY)) {
                        if (tLower === k || k.includes(tLower) || tLower.includes(k)) {
                            matchedKb = v;
                            break;
                        }
                    }
                    const docSentence = sentences.find(s => s.toLowerCase().includes(tLower))?.trim() || "";

                    if (matchedKb) {
                        const s_meaning = targetLang === 'hi' ? matchedKb.simple_meaning : (await clientTranslate(matchedKb.simple_meaning, targetLang)).text;
                        const c_meaning = targetLang === 'hi' ? matchedKb.contextual_meaning : (await clientTranslate(matchedKb.contextual_meaning, targetLang)).text;
                        const ex_meaning = targetLang === 'hi' ? matchedKb.example : (await clientTranslate(matchedKb.example, targetLang)).text;

                        let ans = `📖 शब्द का सीधा अर्थ (Word Meaning):\n• ${matchedKb.term} का सीधा अर्थ है: "${s_meaning}"\n\n💡 सरल व्याख्या:\n${c_meaning}\n\n🌟 दैनिक जीवन का उदाहरण:\n${ex_meaning}`;
                        if (docSentence) {
                            ans += `\n\n📄 इस दस्तावेज़ में संदर्भ:\n"${docSentence}"`;
                        }
                        answerData = {
                            answer: ans,
                            source_passages: docSentence ? [docSentence] : [],
                            found_in_document: Boolean(docSentence)
                        };
                    } else {
                        const tr = await clientTranslate(targetWord, targetLang);
                        let ans = `📖 शब्द का सीधा अर्थ (Word Meaning):\n• ${targetWord.charAt(0).toUpperCase() + targetWord.slice(1)} का सीधा अर्थ है: "${tr.text}"\n\n💡 सरल व्याख्या:\nयह एक सामान्य शब्द है जिसका अर्थ '${tr.text}' होता है।`;
                        if (docSentence) {
                            ans += `\n\n📄 इस दस्तावेज़ में संदर्भ:\n"${docSentence}"`;
                        }
                        answerData = {
                            answer: ans,
                            source_passages: docSentence ? [docSentence] : [],
                            found_in_document: Boolean(docSentence)
                        };
                    }
                } else {
                    const qLower = question.toLowerCase();
                    const keywords = qLower.split(/\s+/).filter(w => w.length > 3);
                    const matches = sentences.filter(s => keywords.some(k => s.toLowerCase().includes(k))).slice(0, 2);

                    if (matches.length > 0) {
                        const passage = matches.join(" ");
                        const ansTr = await clientTranslate(`According to the document: ${passage}`, targetLang);
                        answerData = {
                            answer: ansTr.text,
                            source_passages: matches,
                            found_in_document: true
                        };
                    } else {
                        const notFound = targetLang === "en" ? "This information was not found in the uploaded document." : (await clientTranslate("This information was not found in the uploaded document.", targetLang)).text;
                        answerData = {
                            answer: notFound,
                            source_passages: [],
                            found_in_document: false
                        };
                    }
                }
            }

            // Update thinking message with real answer
            updateChatMessage(thinkingId, answerData.answer, answerData.source_passages);

        } catch (err) {
            updateChatMessage(thinkingId, `Error querying document: ${err.message}`, []);
        }
    }

    function appendChatMessage(type, sender, text) {
        const msgId = `msg_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
        const msgDiv = document.createElement("div");
        msgDiv.id = msgId;
        msgDiv.className = `chat-msg ${type === "user" ? "user-msg" : "ai-msg"}`;
        msgDiv.innerHTML = `
            <div class="msg-sender">${escapeHtml(sender)}</div>
            <div class="msg-text">${escapeHtml(text)}</div>
        `;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return msgId;
    }

    function updateChatMessage(msgId, text, sourcePassages) {
        const msgDiv = document.getElementById(msgId);
        if (!msgDiv) return;

        let passagesHtml = "";
        if (sourcePassages && sourcePassages.length > 0) {
            passagesHtml = sourcePassages.map(p => `<div class="source-passage-box">📄 Source: "${escapeHtml(p)}"</div>`).join("");
        }

        msgDiv.innerHTML = `
            <div class="msg-sender">🤖 Vyron Assistant</div>
            <div class="msg-text">${escapeHtml(text)}</div>
            ${passagesHtml}
        `;
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

/* ==========================================================================
   11. Audio & Speech Synthesis Engine (J.A.R.V.I.S. Cadence & Speed Tuning)
   ========================================================================== */
function initAudioControls() {
    const playBtn = document.getElementById("playAudioBtn");
    const pauseBtn = document.getElementById("pauseAudioBtn");
    const stopBtn = document.getElementById("stopAudioBtn");
    const playIcon = document.getElementById("playAudioIcon");
    const playText = document.getElementById("playAudioText");

    playBtn.addEventListener("click", () => {
        if (state.speechIsPaused) {
            window.speechSynthesis.resume();
            state.speechIsPaused = false;
            pauseBtn.style.display = "inline-flex";
            playBtn.style.display = "none";
            return;
        }

        const purpose = document.getElementById("simpleOverallPurpose").innerText;
        const body = document.getElementById("simpleExplanationBody").innerText;
        const textToRead = `${purpose}. ${body}`;
        const targetLang = document.getElementById("targetLang").value;

        speakText(textToRead, targetLang);
    });

    pauseBtn.addEventListener("click", () => {
        if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
            window.speechSynthesis.pause();
            state.speechIsPaused = true;
            pauseBtn.style.display = "none";
            playBtn.style.display = "inline-flex";
            playText.innerText = "Resume Speech";
        }
    });

    stopBtn.addEventListener("click", () => {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            resetAudioButtons();
        }
    });

    function resetAudioButtons() {
        state.speechIsPaused = false;
        playBtn.style.display = "inline-flex";
        pauseBtn.style.display = "none";
        stopBtn.style.display = "none";
        playIcon.innerText = "🔊";
        playText.innerText = "Play Audio (Jarvis Voice)";
    }

    window.resetAudioButtons = resetAudioButtons;
}

function speakText(text, langCode) {
    if (!('speechSynthesis' in window)) {
        showError("Speech Unsupported", "Your browser does not support Web Speech API synthesis.");
        return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const mappedLang = SPEECH_LANG_MAP[langCode] || 'hi-IN';
    utterance.lang = mappedLang;

    // Resonant pitch and user-controlled rate
    utterance.pitch = 0.2;
    const rateVal = parseFloat(document.getElementById("speechRateSelect")?.value || "0.85");
    utterance.rate = rateVal;

    const voices = window.speechSynthesis.getVoices();
    if (langCode === 'en') {
        const jarvisVoice = voices.find(v => (v.lang === 'en-GB' || v.lang === 'en-UK') && (v.name.includes('Male') || v.name === 'Daniel'));
        if (jarvisVoice) utterance.voice = jarvisVoice;
    } else if (langCode === 'hi') {
        const hiMale = voices.find(v => v.lang.includes('hi') && (v.name.toLowerCase().includes('male') || v.name.includes('Rishi')));
        if (hiMale) utterance.voice = hiMale;
    }

    const playBtn = document.getElementById("playAudioBtn");
    const pauseBtn = document.getElementById("pauseAudioBtn");
    const stopBtn = document.getElementById("stopAudioBtn");

    utterance.onstart = () => {
        playBtn.style.display = "none";
        pauseBtn.style.display = "inline-flex";
        stopBtn.style.display = "inline-flex";
    };

    utterance.onend = () => {
        if (window.resetAudioButtons) window.resetAudioButtons();
    };

    utterance.onerror = () => {
        if (window.resetAudioButtons) window.resetAudioButtons();
    };

    state.speechUtterance = utterance;
    window.speechSynthesis.speak(utterance);
}

/* ==========================================================================
   12. Interactive Features: "Explain More Simply" & Custom Term Decoder
   ========================================================================== */
function initExplanationSimplifier() {
    const simplifyBtn = document.getElementById("simplifyMoreBtn");
    simplifyBtn.addEventListener("click", async () => {
        const purpose = document.getElementById("simpleOverallPurpose").innerText;
        const targetLang = document.getElementById("targetLang").value;

        simplifyBtn.innerText = "⚡ Simplifying further...";
        simplifyBtn.disabled = true;

        try {
            if (state.isBackendOnline) {
                const res = await fetch(`${state.backendUrl}/api/simplify-more`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ paragraph: purpose, target_lang: targetLang })
                });
                if (res.ok) {
                    const data = await res.json();
                    insertSimplifiedAnalogyBox(data.simplified_text, data.analogy);
                    return;
                }
            }

            // Fallback simplification
            insertSimplifiedAnalogyBox(
                `सीधे शब्दों में: यह एक औपचारिक सरकारी नोटिस है जिसे दी गई समय सीमा से पहले पूरा करना अनिवार्य है।`,
                `जैसे स्कूल का होमवर्क आखिरी तारीख से पहले जमा करना जरूरी होता है, वैसे ही यह प्रक्रिया पूरी करें।`
            );
        } catch (e) {
            // Non-fatal
        } finally {
            simplifyBtn.innerText = "⚡ Explain More Simply";
            simplifyBtn.disabled = false;
        }
    });

    function insertSimplifiedAnalogyBox(text, analogy) {
        let box = document.getElementById("superSimpleAnalogyBox");
        if (!box) {
            box = document.createElement("div");
            box.id = "superSimpleAnalogyBox";
            box.style.background = "rgba(195, 255, 0, 0.08)";
            box.style.border = "1px solid var(--primary)";
            box.style.borderRadius = "var(--radius-md)";
            box.style.padding = "16px";
            box.style.margin = "14px 0";
            const purposeBox = document.querySelector(".purpose-highlight-box");
            if (purposeBox) {
                purposeBox.parentNode.insertBefore(box, purposeBox.nextSibling);
            }
        }
        box.innerHTML = `
            <div style="font-size: 0.8rem; font-weight: 800; color: var(--primary); margin-bottom: 6px;">👶 5TH-GRADER EVERYDAY TRANSLATION</div>
            <p style="font-size: 1.05rem; font-weight: 600; color: #fff; margin-bottom: 8px;">${escapeHtml(text)}</p>
            ${analogy ? `<div style="font-size: 0.88rem; color: var(--text-muted); font-style: italic;">💡 Analogy: ${escapeHtml(analogy)}</div>` : ''}
        `;
        box.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
}

function initCustomTermExplainer() {
    const input = document.getElementById("customTermInput");
    const btn = document.getElementById("explainCustomTermBtn");

    btn.addEventListener("click", async () => {
        const term = input.value.trim();
        if (!term) return;

        btn.innerText = "Decoding...";
        btn.disabled = true;

        const targetLang = document.getElementById("targetLang").value;
        const context = state.extractedSourceText ? state.extractedSourceText.slice(0, 300) : "";

    // 1. Check authoritative Civic Knowledge Base dictionary first
    const tLower = term.toLowerCase();
    let matchedKb = null;
    for (const [k, v] of Object.entries(CIVIC_CLIENT_DICTIONARY)) {
        if (tLower === k || tLower.includes(k) || k.includes(tLower)) {
            matchedKb = v;
            break;
        }
    }

    try {
        let termResult = null;

        if (matchedKb) {
            const s_meaning = targetLang === 'hi' ? matchedKb.simple_meaning : (await clientTranslate(matchedKb.simple_meaning, targetLang)).text;
            const c_meaning = targetLang === 'hi' ? matchedKb.contextual_meaning : (await clientTranslate(matchedKb.contextual_meaning, targetLang)).text;
            const ex_meaning = targetLang === 'hi' ? matchedKb.example : (await clientTranslate(matchedKb.example, targetLang)).text;
            termResult = {
                term: matchedKb.term,
                simple_meaning: s_meaning,
                contextual_meaning: c_meaning,
                example: ex_meaning,
                source_sentence: context || `Appears in document context for '${term}'.`
            };
        } else if (state.isBackendOnline) {
            const res = await fetch(`${state.backendUrl}/api/explain-term`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ term, context, target_lang: targetLang })
            });
            if (res.ok) {
                termResult = await res.json();
            }
        }

        if (!termResult) {
            const tr = await clientTranslate(term, targetLang);
            const directMeaning = tr.text || term;
            termResult = {
                term: `${term} (${directMeaning})`,
                simple_meaning: targetLang === 'hi' ? `सीधा अर्थ: "${directMeaning}"` : `Direct meaning: "${directMeaning}"`,
                contextual_meaning: context ? (await clientTranslate(context, targetLang)).text : (targetLang === 'hi' ? `दस्तावेज़ में प्रयुक्त शब्द।` : `Used in document context.`),
                example: targetLang === 'hi' ? `दैनिक जीवन में इसका अर्थ '${directMeaning}' होता है।` : `Commonly understood as '${directMeaning}'.`,
                source_sentence: context || `User search.`
            };
        }

            const jargonGrid = document.getElementById("jargonCardsContainer");
            const card = document.createElement("div");
            card.className = "jargon-card";
            card.style.borderColor = "var(--primary)";
            card.innerHTML = `
                <div class="jargon-card-top">
                    <span class="jargon-term">${escapeHtml(termResult.term)} <span class="badge badge-accent">Searched</span></span>
                    <button class="icon-btn speak-term-btn" type="button" data-term="${escapeHtml(termResult.term)}" data-meaning="${escapeHtml(termResult.simple_meaning)}">
                        🔊 Read
                    </button>
                </div>
                <div class="jargon-meaning">👉 ${escapeHtml(termResult.simple_meaning)}</div>
                <div class="jargon-context"><strong>Context:</strong> ${escapeHtml(termResult.contextual_meaning)}</div>
                ${termResult.example ? `<div class="jargon-example"><strong>Example:</strong> ${escapeHtml(termResult.example)}</div>` : ''}
            `;
            jargonGrid.prepend(card);

            card.querySelector(".speak-term-btn").addEventListener("click", () => {
                speakText(`${termResult.term}. ${termResult.simple_meaning}`, targetLang);
            });

            input.value = "";
            card.scrollIntoView({ behavior: "smooth", block: "nearest" });

        } catch (e) {
            showError("Term Lookup Failed", e.message);
        } finally {
            btn.innerText = "Decode Term";
            btn.disabled = false;
        }
    });
}

/* ==========================================================================
   13. Reset, Copy & Export Actions
   ========================================================================== */
function initResetAndCopy() {
    // Copy Simple Meaning Summary
    document.getElementById("copySimpleBtn").addEventListener("click", () => {
        const purpose = document.getElementById("simpleOverallPurpose").innerText;
        const body = document.getElementById("simpleExplanationBody").innerText;
        copyToClipboard(`${purpose}\n\n${body}`);
    });

    // Copy Translation All
    document.getElementById("copyTranslatedBtn").addEventListener("click", () => {
        const text = document.getElementById("literalTranslationBox").innerText;
        copyToClipboard(text);
    });

    // Copy Raw Source Text
    document.getElementById("copySourceBtn").addEventListener("click", () => {
        const text = document.getElementById("rawSourceTextBox").innerText;
        copyToClipboard(text);
    });

    // Download Complete Intelligence Report (.txt)
    document.getElementById("downloadReportBtn").addEventListener("click", () => {
        if (!state.lastAnalysisData) return;
        const analysis = state.lastAnalysisData.analysis || {};
        const report = `=====================================================
VYRON AI 2.0 — PUBLIC DOCUMENT INTELLIGENCE REPORT
=====================================================

DOCUMENT TYPE: ${analysis.document_type || "Official Notice"}
TARGET LANGUAGE: ${state.lastAnalysisData.target_lang || "hi"}

-----------------------------------------------------
1. CORE PURPOSE & CITIZEN SUMMARY:
-----------------------------------------------------
${analysis.simple_explanation?.overall_purpose || ""}

${analysis.simple_explanation?.simplified_body || ""}

-----------------------------------------------------
2. WHAT YOU NEED TO DO (ACTION MATRIX):
-----------------------------------------------------
* DEADLINE: ${analysis.what_you_need_to_do?.deadlines || "Not specified in document"}
* FEES / PAYMENTS: ${analysis.what_you_need_to_do?.fees_and_payments || "Not specified in document"}
* REQUIRED DOCUMENTS: ${JSON.stringify(analysis.what_you_need_to_do?.required_documents || "Not specified")}
* PENALTIES / WARNINGS: ${analysis.what_you_need_to_do?.penalties_or_consequences || "Not specified"}

REQUIRED ACTIONS:
${(analysis.what_you_need_to_do?.required_actions || []).map((a, i) => `${i + 1}. ${a}`).join("\n")}

-----------------------------------------------------
3. DECODED JARGON TERMS:
-----------------------------------------------------
${(analysis.jargon_decoded || []).map(j => `* ${j.term}: ${j.simple_meaning}\n  Context: ${j.contextual_meaning}`).join("\n\n")}

-----------------------------------------------------
4. FULL FAITHFUL TRANSLATION:
-----------------------------------------------------
${state.lastAnalysisData.faithful_translation || state.lastAnalysisData.literal_translated_text || ""}

=====================================================
Generated by VYRON AI 2.0 (Open-Weight Public Intelligence)
=====================================================`;

        downloadBlob(report, `Vyron_Intelligence_Report_${Date.now()}.txt`, "text/plain;charset=utf-8");
    });

    // Export Structured JSON (.json)
    document.getElementById("downloadJsonBtn").addEventListener("click", () => {
        if (!state.lastAnalysisData) return;
        const jsonStr = JSON.stringify(state.lastAnalysisData, null, 2);
        downloadBlob(jsonStr, `Vyron_Analysis_${Date.now()}.json`, "application/json;charset=utf-8");
    });

    // Reset Workflow
    document.getElementById("resetWorkflowBtn").addEventListener("click", () => {
        document.getElementById("resultsWrapper").style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Clear Document & Memory
    document.getElementById("clearMemoryBtn").addEventListener("click", () => {
        document.getElementById("sourceText").value = "";
        document.getElementById("charCount").innerText = "0 characters";
        document.getElementById("removePdfBtn")?.click();
        document.getElementById("removeImageBtn")?.click();
        state.selectedFile = null;
        state.extractedSourceText = "";
        state.lastAnalysisData = null;
        document.getElementById("resultsWrapper").style.display = "none";
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

function copyToClipboard(text) {
    if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            alert("Copied to clipboard! 📋");
        }).catch(() => {
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    alert("Copied to clipboard! 📋");
}

function downloadBlob(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
}

/* ==========================================================================
   14. Modal & Error Handling Utilities
   ========================================================================== */
function initModal() {
    const configBtn = document.getElementById("configHelpBtn");
    const modal = document.getElementById("configModal");
    const closeBtn = document.getElementById("closeConfigModalBtn");

    configBtn.addEventListener("click", () => {
        modal.style.display = "flex";
        initEngineHealthCheck();
    });

    closeBtn.addEventListener("click", () => modal.style.display = "none");
    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.style.display = "none";
    });
}

function showError(title, message) {
    const banner = document.getElementById("errorBanner");
    document.getElementById("errorTitle").innerText = title;
    document.getElementById("errorMsg").innerText = message;
    banner.style.display = "flex";
    banner.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function hideError() {
    document.getElementById("errorBanner").style.display = "none";
}

function escapeHtml(unsafe) {
    if (!unsafe) return "";
    return String(unsafe)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Service Worker Registration for Offline Cache & Installability
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js').catch(() => {});
    });
}
