import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowRight, BarChart3, Bell, CheckCircle2, ChevronLeft, CircleDollarSign,
  CreditCard, ExternalLink, Eye, Grid2X2, LayoutDashboard, MessageCircle,
  Minus, Monitor, PackageCheck, Plus, Search, ShoppingCart, SlidersHorizontal,
  Smartphone, Sparkles, Store, Users, Warehouse, X, Zap
} from "lucide-react";
import { Button } from "../components/Button";
import styles from "./_index.module.css";

type PackageId = "start" | "business" | "pro";
type DemoView = "store" | "admin";
type DeviceMode = "desktop" | "mobile";
type ProTheme = "elinour" | "italian";

const packageData = {
  start: {
    id: "start" as const,
    name: "Mini",
    price: "2,500",
    tone: "bronze",
    label: "Smart Entry",
    description: "متجر متجاوب للموبايل والكمبيوتر، حتى 20 منتجًا عند التسليم، أقسام وصور وأسعار، وطلب مباشر عبر واتساب.",
    highlights: ["Responsive Storefront", "Up to 20 Products", "WhatsApp Ordering"],
    reference: "Mini Commerce Package",
  },
  business: {
    id: "business" as const,
    name: "Smart",
    price: "3,500",
    tone: "silver",
    label: "Most Popular",
    description: "حتى 50 منتجًا عند التسليم، بحث وتصنيفات وسلة مشتريات، إدارة منتجات وأسعار وعروض، وتنظيم مبسط للطلبات.",
    highlights: ["Search + Categories", "Shopping Cart", "Product Management"],
    reference: "Smart Commerce Package",
  },
  pro: {
    id: "pro" as const,
    name: "Smart Plus",
    price: "4,900",
    tone: "gold",
    label: "Best Value",
    description: "حتى 100 منتج عند التسليم، لوحة إدارة للمنتجات والطلبات، بيانات العملاء وحالة الطلب، إعدادات أساسية ودعم إطلاق.",
    highlights: ["Store + Admin", "Orders + Customers", "Launch Support"],
    reference: "Smart Plus Commerce Package",
  },
};

const projects = [
  {
    name: "BARIQ",
    arabic: "بريق",
    tier: "Business",
    url: "https://bariq-store.mamod-elhag.chatgpt.site",
    tag: "E-Commerce",
    description: "متجر بيع أونلاين بواجهة منظمة وتجربة موبايل واضحة، مصمم للوصول للمنتج والطلب بأقل خطوات.",
    bullets: ["Responsive Store", "Product Experience", "Business UI"],
    accent: "bariq",
  },
  {
    name: "ELINOUR",
    arabic: "الينور",
    tier: "Business Pro",
    url: "https://elinor-perfumes.floot.app",
    tag: "Luxury Perfume Store",
    description: "متجر عطور فاخر بهوية Premium داكنة، Storefront مستقلة ولوحة إدارة منفصلة للمنتجات والطلبات.",
    bullets: ["Luxury Branding", "Store + Admin", "Mobile Ready"],
    accent: "elinour",
  },
  {
    name: "ITALIAN COMPANY",
    arabic: "الشركة الإيطالية",
    tier: "Business Pro + Custom",
    url: "https://italian-company-renault-parts.floot.app",
    tag: "Auto Parts Platform",
    description: "منصة قطع غيار رينو بمتجر، إدارة متقدمة، CRM، مخزون، دفع InstaPay، تقارير وتتبع للطلبات.",
    bullets: ["CRM + Inventory", "Payments", "Order Tracking"],
    accent: "italian",
  },
];

const startProducts = [
  { id:"s1", name:"حقيبة جلد أنيقة", sub:"جلد فاخر • تصميم يومي", price:1950, category:"حقائب", stock:15, image:"https://hag-studio-portfolio.floot.app/_cdn/static/69aa6ce1-3b45-4449-aa6e-a07ec8d39c90.png" },
  { id:"s2", name:"عطر فاخر", sub:"رائحة دافئة • ثبات طويل", price:1350, category:"عطور", stock:9, image:"https://hag-studio-portfolio.floot.app/_cdn/static/fb3e01ab-4bee-44a8-a295-8ded96896a9e.png" },
  { id:"s3", name:"ساعة كلاسيكية", sub:"تصميم أنيق • استخدام يومي", price:1750, category:"ساعات", stock:8, image:"https://hag-studio-portfolio.floot.app/_cdn/static/c672c5ad-ea08-4522-83b5-79e6f60fac35.png" },
  { id:"s4", name:"محفظة جلد طبيعي", sub:"جلد طبيعي • تصميم عملي", price:750, category:"محافظ", stock:22, image:"https://hag-studio-portfolio.floot.app/_cdn/static/4cb42891-2b3e-4fbb-8b39-275f38fed645.png" },
];

const businessProducts = [
  { id:"b1", name:"حقيبة Signature", sub:"Premium Leather Collection", price:2250, category:"الأكثر طلبًا", stock:18, image:"https://hag-studio-portfolio.floot.app/_cdn/static/69aa6ce1-3b45-4449-aa6e-a07ec8d39c90.png" },
  { id:"b2", name:"عطر Rose Edition", sub:"New Arrival • 75ml", price:1650, category:"جديد", stock:12, image:"https://hag-studio-portfolio.floot.app/_cdn/static/fb3e01ab-4bee-44a8-a295-8ded96896a9e.png" },
  { id:"b3", name:"ساعة Executive", sub:"Classic Series", price:2850, category:"مميز", stock:7, image:"https://hag-studio-portfolio.floot.app/_cdn/static/c672c5ad-ea08-4522-83b5-79e6f60fac35.png" },
  { id:"b4", name:"محفظة Urban", sub:"Natural Leather", price:980, category:"الكل", stock:24, image:"https://hag-studio-portfolio.floot.app/_cdn/static/4cb42891-2b3e-4fbb-8b39-275f38fed645.png" },
];

const elinourProducts = [
  { id:"e1", name:"Velvet Oud", sub:"50ml • Oriental", price:1850, category:"عود", stock:8, image:"https://hag-studio-portfolio.floot.app/_cdn/static/dd4beeb6-256e-409d-8c40-db8325517d4c.png" },
  { id:"e2", name:"Noir 01", sub:"75ml • Signature", price:2450, category:"Signature", stock:5, image:"https://hag-studio-portfolio.floot.app/_cdn/static/fb3e01ab-4bee-44a8-a295-8ded96896a9e.png" },
  { id:"e3", name:"Amber Musk", sub:"50ml • Warm", price:1650, category:"مسك", stock:11, image:"https://hag-studio-portfolio.floot.app/_cdn/static/dd4beeb6-256e-409d-8c40-db8325517d4c.png" },
  { id:"e4", name:"Elinour Privé", sub:"100ml • Exclusive", price:3250, category:"Privé", stock:3, image:"https://hag-studio-portfolio.floot.app/_cdn/static/fb3e01ab-4bee-44a8-a295-8ded96896a9e.png" },
];

const italianProducts = [
  { id:"i1", name:"موتور K7M كامل", sub:"Logan • 2015–2019", price:38500, category:"مواتير", stock:2, image:"https://hag-studio-portfolio.floot.app/_cdn/static/8b4e613a-82af-4b6a-ad5c-f1e1318ada62.png" },
  { id:"i2", name:"فتيس DP0", sub:"Megane III • 2012–2016", price:24750, category:"فتيس", stock:3, image:"https://hag-studio-portfolio.floot.app/_cdn/static/3b7e7d6a-0659-405b-bbac-afd6a3494d9e.png" },
  { id:"i3", name:"كمبروسر تكييف", sub:"Fluence • 2014–2017", price:7200, category:"تكييف", stock:5, image:"https://hag-studio-portfolio.floot.app/_cdn/static/3d73461f-0bc5-45a1-ad04-df6e3bfc3b19.png" },
  { id:"i4", name:"علبة دركسيون كهرباء", sub:"Sandero • 2016–2020", price:9800, category:"عفشة", stock:4, image:"https://hag-studio-portfolio.floot.app/_cdn/static/8b4e613a-82af-4b6a-ad5c-f1e1318ada62.png" },
];

function PackageSnapshot({pkg}:{pkg:PackageId}){
  const products = pkg==="start" ? startProducts : pkg==="business" ? businessProducts : elinourProducts;
  const labels = pkg==="start"
    ? ["STORE","PRODUCTS","ORDERS"]
    : pkg==="business"
      ? ["STORE","SEARCH","CART","DASHBOARD"]
      : ["STORE","CRM","STOCK","PAYMENTS","REPORTS"];
  return <div className={styles.snapshot}>
    <div className={styles.snapshotBar}><i/><i/><i/><span>{pkg}.hag-demo.app</span></div>
    <div className={styles.snapshotLayout}>
      <div className={styles.snapshotStore}>
        <div className={styles.snapshotNav}><b>{pkg==="pro"?"PREMIUM STORE":"ONLINE STORE"}</b><ShoppingCart/></div>
        <div className={styles.snapshotHero}><img src={products[0].image} alt=""/><div><span/><b/><small/></div></div>
        <div className={styles.snapshotProducts}>{products.slice(0,3).map(p=><i key={p.id}><img src={p.image} alt=""/></i>)}</div>
      </div>
      <div className={styles.snapshotAdmin}>
        <LayoutDashboard/>
        <div><b>ADMIN</b>{labels.slice(1).map(x=><span key={x}>{x}</span>)}</div>
      </div>
    </div>
  </div>
}

function StoreDemo({pkg}:{pkg:PackageId}){
  const [query,setQuery]=useState("");
  const [category,setCategory]=useState("الكل");
  const [cart,setCart]=useState<Record<string,number>>({});
  const [cartOpen,setCartOpen]=useState(false);
  const [proTheme,setProTheme]=useState<ProTheme>("italian");

  const source = pkg==="start" ? startProducts : pkg==="business" ? businessProducts : proTheme==="elinour" ? elinourProducts : italianProducts;
  const categories = ["الكل",...Array.from(new Set(source.map(p=>p.category).filter(x=>x!=="الكل")))];
  const shown = useMemo(()=>source.filter(p=>{
    const q=(p.name+" "+p.sub).toLowerCase();
    const categoryOk=category==="الكل"||p.category===category;
    return categoryOk&&q.includes(query.toLowerCase());
  }),[source,query,category]);
  const count=Object.values(cart).reduce((a,b)=>a+b,0);
  const total=source.reduce((s,p)=>s+p.price*(cart[p.id]||0),0);
  const add=(id:string)=>setCart(c=>({...c,[id]:(c[id]||0)+1}));
  const setQty=(id:string,n:number)=>setCart(c=>{const next={...c};if(n<=0)delete next[id];else next[id]=n;return next;});

  const brand = pkg==="start" ? "LUMORA" : pkg==="business" ? "BARIQ" : proTheme==="elinour" ? "ELINOUR" : "ITALIAN COMPANY";
  const heroTitle = pkg==="start"
    ? "أناقة ترافقك في كل لحظة."
    : pkg==="business"
      ? "تصفح أسرع. بحث أذكى. سلة أوضح."
      : proTheme==="elinour"
        ? "Luxury shopping built around the brand."
        : "قطع رينو أصلية. مختارة بعناية.";
  const heroImage = pkg==="start"
    ? startProducts[0].image
    : pkg==="business"
      ? businessProducts[1].image
      : proTheme==="elinour"
        ? elinourProducts[0].image
        : italianProducts[0].image;

  return <div className={[styles.storeDemo,styles["store"+pkg],pkg==="pro"?styles["theme"+proTheme]:""].join(" ")}>
    <header className={styles.storeHeader}>
      <div className={styles.storeBrand}><span>{brand.slice(0,1)}</span><div><b>{brand}</b><small>{pkg==="pro"?"PREMIUM COMMERCE":"ONLINE STORE"}</small></div></div>
      <nav><button>الرئيسية</button><button>المنتجات</button>{pkg!=="start"&&<button>التصنيفات</button>}{pkg==="pro"&&<button>تتبع طلبك</button>}</nav>
      <button className={styles.storeCartBtn} onClick={()=>setCartOpen(true)}><ShoppingCart/><span>السلة</span><b>{count}</b></button>
    </header>

    {pkg==="pro"&&<div className={styles.themeSwitch}>
      <span>REAL-WORK INSPIRED THEMES</span>
      <div><button className={proTheme==="italian"?styles.themeActive:""} onClick={()=>{setProTheme("italian");setCategory("الكل");setQuery("");}}>Italian Company</button><button className={proTheme==="elinour"?styles.themeActive:""} onClick={()=>{setProTheme("elinour");setCategory("الكل");setQuery("");}}>ELINOUR</button></div>
    </div>}

    <section className={styles.storeHero}>
      <div><span>{pkg==="pro"?"BUILT FROM REAL CLIENT WORK":"HAG STUDIO EXPERIENCE"}</span><h3>{heroTitle}</h3><p>{pkg==="start"?"واجهة متجر حقيقية بمنتجات وصور وأسعار وسلة شغالة من أول يوم.":pkg==="business"?"واجهة منظمة مع Search + Filters + Cart editable وتجربة شراء أسرع.":"هوية مخصصة، تجربة حسب النشاط، Checkout متقدم وربط واضح مع الإدارة."}</p><button onClick={()=>document.querySelector("[data-demo-products]")?.scrollIntoView({behavior:"smooth",block:"nearest"})}>استكشف المنتجات <ChevronLeft/></button></div>
      <div className={styles.storeHeroVisual}><img src={heroImage} alt="منتج مميز"/><span>{pkg==="pro"?"CUSTOM":"RESPONSIVE"}</span></div>
    </section>

    {pkg!=="start"&&<div className={styles.storeTools}>
      <div className={styles.storeSearch}><Search/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="ابحث بالاسم أو التفاصيل..."/><SlidersHorizontal/></div>
      <div className={styles.storeCategories}>{categories.map(c=><button key={c} className={category===c?styles.categoryActive:""} onClick={()=>setCategory(c)}>{c}</button>)}</div>
    </div>}

    <div className={styles.storeGrid} data-demo-products>
      {shown.map((p,i)=><article key={p.id} className={styles.storeProduct}>
        <div className={styles.storeProductVisual}><span>{pkg==="pro"&&proTheme==="italian"?"OEM":pkg==="pro"&&proTheme==="elinour"?"EAU":"0"+(i+1)}</span><img src={p.image} alt={p.name}/></div>
        <div className={styles.storeProductBody}><small>{p.category}</small><h4>{p.name}</h4><p>{p.sub}</p><div><b>{p.price.toLocaleString("en-US")} ج</b><button onClick={()=>add(p.id)}>{cart[p.id]?"أضف مرة أخرى":"أضف للسلة"}</button></div></div>
      </article>)}
    </div>

    {pkg==="pro"&&<div className={styles.storeValueStrip}>
      <div><CreditCard/><span>Cash / InstaPay</span></div><div><PackageCheck/><span>Order Tracking</span></div><div><Warehouse/><span>Live Stock</span></div>
    </div>}

    {cartOpen&&<div className={styles.demoCartBackdrop} onClick={()=>setCartOpen(false)}>
      <aside className={styles.demoCartDrawer} onClick={e=>e.stopPropagation()}>
        <div className={styles.demoCartHead}><div><span>YOUR CART</span><h4>سلة الطلب</h4><small>{count} قطعة</small></div><button onClick={()=>setCartOpen(false)}><X/></button></div>
        <div className={styles.demoCartItems}>
          {Object.keys(cart).length===0?<div className={styles.demoEmpty}>أضف منتجات علشان تشوف تجربة السلة.</div>:source.filter(p=>cart[p.id]).map(p=><div key={p.id}>
            <div><b>{p.name}</b><span>{p.sub}</span></div>
            <div className={styles.demoQty}><button onClick={()=>setQty(p.id,(cart[p.id]||0)-1)}><Minus/></button><b>{cart[p.id]}</b><button onClick={()=>setQty(p.id,(cart[p.id]||0)+1)}><Plus/></button></div>
            <strong>{(p.price*(cart[p.id]||0)).toLocaleString("en-US")} ج</strong>
          </div>)}
        </div>
        <div className={styles.demoCartSummary}><span>الإجمالي</span><b>{total.toLocaleString("en-US")} ج</b></div>
        {pkg==="pro"&&<div className={styles.demoPaymentChoice}><button className={styles.payActive}><CreditCard/> InstaPay / تحويل</button><button>الدفع عند الاستلام</button></div>}
        <button className={styles.demoCheckoutBtn} disabled={!count}>تأكيد الطلب</button>
      </aside>
    </div>}
  </div>
}

function AdminDemo({pkg}:{pkg:PackageId}){
  const [tab,setTab]=useState(pkg==="start"?"products":"dashboard");
  const [selectedOrder,setSelectedOrder]=useState<string|null>(null);
  const [adding,setAdding]=useState(false);
  const [editingProduct,setEditingProduct]=useState<string|null>(null);
  const adminProducts = pkg==="start" ? startProducts : pkg==="business" ? businessProducts : italianProducts;
  const editing = adminProducts.find(p=>p.id===editingProduct);
  const tabs = pkg==="start"
    ? [["products","المنتجات"],["orders","الطلبات"]]
    : pkg==="business"
      ? [["dashboard","الرئيسية"],["orders","الطلبات"],["products","المنتجات"],["customers","العملاء"]]
      : [["dashboard","الرئيسية"],["orders","الطلبات"],["customers","CRM"],["inventory","المخزون"],["payments","الدفع"],["reports","التقارير"]];

  return <div className={[styles.adminDemo,styles["admin"+pkg]].join(" ")}>
    <aside>
      <div className={styles.adminLogo}><LayoutDashboard/><div><b>HAG CONTROL</b><small>{packageData[pkg].name}</small></div></div>
      <nav>{tabs.map(([id,label])=><button key={id} className={tab===id?styles.adminActive:""} onClick={()=>setTab(id)}><span>{label}</span>{id==="orders"&&<b>3</b>}</button>)}</nav>
      <div className={styles.adminSideFoot}><i/> SYSTEM ONLINE</div>
    </aside>
    <section className={styles.adminMain}>
      <header className={styles.adminHeader}>
        <div><small>{packageData[pkg].name.toUpperCase()} BUSINESS CONTROL</small><h3>{tabs.find(x=>x[0]===tab)?.[1]}</h3></div>
        <div><button><Bell/><i/></button><span>LIVE</span></div>
      </header>

      {tab==="dashboard"&&<div className={styles.adminDashboard}>
        <div className={styles.adminKpis}>
          <article><CircleDollarSign/><span>المبيعات</span><b>{pkg==="pro"?"126,850":"48,350"} ج</b><small>+12.4%</small></article>
          <article><ShoppingCart/><span>الطلبات</span><b>{pkg==="pro"?"64":"27"}</b><small>Live Orders</small></article>
          <article><Users/><span>العملاء</span><b>{pkg==="pro"?"184":"73"}</b><small>Customer Base</small></article>
          {pkg==="pro"&&<article><Warehouse/><span>المخزون</span><b>96%</b><small>Stock Health</small></article>}
        </div>
        <div className={styles.dashboardBody}>
          <div className={styles.chartCard}><div><span>SALES PERFORMANCE</span><b>نمو المبيعات</b></div><div className={styles.lineChart}><svg viewBox="0 0 500 170" preserveAspectRatio="none"><polyline points="0,135 65,118 125,128 195,88 255,102 315,60 380,74 440,35 500,48" fill="none" stroke="currentColor" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round"/></svg><div/><div/><div/><div/><div/></div></div>
          <div className={styles.activityCard}><span>RECENT ACTIVITY</span><b>آخر حركة</b>{["طلب جديد تم استلامه","تم تحديث منتج","عميل عاد للشراء"].map((x,i)=><div key={x}><i/><p>{x}<small>منذ {i+1} دقائق</small></p></div>)}</div>
        </div>
      </div>}

      {tab==="products"&&<div className={styles.adminWorkspace}>
        <div className={styles.workspaceToolbar}><div><span>PRODUCT MANAGEMENT</span><b>إدارة المنتجات</b></div><button onClick={()=>{setAdding(!adding);setEditingProduct(null);}}><Plus/> إضافة منتج</button></div>
        {(adding||editing)&&<div className={styles.quickForm}><input defaultValue={editing?.name||""} placeholder="اسم المنتج"/><input defaultValue={editing?String(editing.price):""} placeholder="السعر"/><input defaultValue={editing?String(editing.stock):""} placeholder="المخزون"/><button onClick={()=>{setAdding(false);setEditingProduct(null);}}>حفظ التعديل</button></div>}
        <div className={styles.adminProductList}>{adminProducts.slice(0,pkg==="start"?4:4).map((p,i)=><div key={p.id}><div className={styles.adminProductThumb}><img src={p.image} alt={p.name}/></div><div><b>{p.name}</b><span>SKU-{pkg.toUpperCase()}-{103+i}</span></div><small>{p.stock} متاح</small><strong>{p.price.toLocaleString("en-US")} ج</strong><button onClick={()=>{setEditingProduct(p.id);setAdding(false);}}><Eye/> تعديل</button></div>)}</div>
      </div>}

      {tab==="orders"&&<div className={styles.adminWorkspace}>
        <div className={styles.workspaceToolbar}><div><span>ORDER FLOW</span><b>الطلبات الحالية</b></div><span className={styles.livePill}>3 NEW</span></div>
        <div className={styles.orderCards}>{["ORD-2041","ORD-2040","ORD-2039"].map((id,i)=><article key={id}>
          <div><code>{id}</code><b>{["أحمد محمد","محمود علي","سارة خالد"][i]}</b><small>010 •••• {2431+i}</small></div>
          <span className={styles["status"+i]}>{["طلب جديد","جارٍ التجهيز","تم الشحن"][i]}</span>
          <strong>{(3650+i*2450).toLocaleString("en-US")} ج</strong>
          <button onClick={()=>setSelectedOrder(id)}>تفاصيل</button>
        </article>)}</div>
      </div>}

      {tab==="customers"&&<div className={styles.adminWorkspace}>
        <div className={styles.workspaceToolbar}><div><span>{pkg==="pro"?"ADVANCED CRM":"CUSTOMERS"}</span><b>{pkg==="pro"?"CRM وتصنيف العملاء":"إدارة العملاء"}</b></div></div>
        <div className={styles.crmGrid}>{(pkg==="pro"?[["VIP",24],["Returning",86],["First-Time",23],["New",51]]:[["متكرر",38],["جديد",35]]).map(([x,n])=><article key={String(x)}><span>{x}</span><b>{n}</b><small>{pkg==="pro"?"Customer Segment":"Customer Group"}</small></article>)}</div>
        <div className={styles.crmTable}>{["عميل مميز","عميل متكرر","عميل جديد"].map((x,i)=><div key={x}><div><b>{x}</b><span>010 •••• {630+i}</span></div><span>{[7,4,1][i]} طلبات</span><strong>{[28450,13200,3650][i].toLocaleString("en-US")} ج</strong></div>)}</div>
      </div>}

      {tab==="inventory"&&<div className={styles.adminWorkspace}><div className={styles.workspaceToolbar}><div><span>LIVE INVENTORY</span><b>المخزون والمشتريات</b></div><button><Plus/> تسجيل مشتريات</button></div><div className={styles.inventoryHero}><Warehouse/><div><span>STOCK HEALTH</span><b>128 قطعة متاحة</b><p>7 قطع وصلت لحد المخزون المنخفض وتحتاج متابعة.</p></div></div><div className={styles.stockRows}>{[["موتور K7M",2,2],["فتيس DP0",3,2],["كمبروسر",5,2]].map(([n,q,min])=><div key={String(n)}><b>{n}</b><span>المتاح {q}</span><div><i style={{width:(Number(q)/6*100)+"%"}}/></div><small>Low stock: {min}</small></div>)}</div></div>}

      {tab==="payments"&&<div className={styles.adminWorkspace}><div className={styles.workspaceToolbar}><div><span>PAYMENT CENTER</span><b>إدارة الدفع والتحويلات</b></div></div><div className={styles.paymentKpis}><article><span>المحصل</span><b>81,300 ج</b></article><article><span>بانتظار المراجعة</span><b>4 تحويلات</b></article><article><span>Cash on Delivery</span><b>18 طلب</b></article></div><div className={styles.paymentReview}><CreditCard/><div><b>InstaPay / Bank Transfer</b><span>إيصال جديد بانتظار المراجعة</span></div><button>مراجعة الإيصال</button></div></div>}

      {tab==="reports"&&<div className={styles.adminWorkspace}><div className={styles.workspaceToolbar}><div><span>REPORTING CENTER</span><b>تقارير المبيعات والأداء</b></div><button>Export CSV</button></div><div className={styles.reportCards}><article><BarChart3/><span>مبيعات الشهر</span><b>126,850 ج</b></article><article><CircleDollarSign/><span>المحصل فعليًا</span><b>81,300 ج</b></article><article><ShoppingCart/><span>عدد الطلبات</span><b>64</b></article></div><div className={styles.reportChart}>{[42,68,54,82,64,91,78,100,86,112,96,126].map((n,i)=><i key={i} style={{height:Math.min(n,100)+"%"}}/> )}</div></div>}

      {selectedOrder&&<div className={styles.orderDetailBackdrop} onClick={()=>setSelectedOrder(null)}><div className={styles.orderDetail} onClick={e=>e.stopPropagation()}><div><span>ORDER DETAILS</span><h4>{selectedOrder}</h4><button onClick={()=>setSelectedOrder(null)}><X/></button></div><section><p><span>العميل</span><b>أحمد محمد</b></p><p><span>الإجمالي</span><b>8,550 ج</b></p><p><span>الحالة</span><b>جارٍ التجهيز</b></p>{pkg==="pro"&&<p><span>الدفع</span><b>InstaPay • مدفوع</b></p>}</section><article><b>تفاصيل الطلب</b><span>{adminProducts[0]?.name} × 1</span><span>{adminProducts[1]?.name} × 2</span></article><button className={styles.orderDone} onClick={()=>setSelectedOrder(null)}>تمت المراجعة</button></div></div>}
    </section>
  </div>
}

export default function PortfolioPage(){
  const [selected,setSelected]=useState<PackageId>("business");
  const [view,setView]=useState<DemoView>("store");
  const [device,setDevice]=useState<DeviceMode>("desktop");
  const [demoOpen,setDemoOpen]=useState(false);

  const openDemo=(pkg:PackageId,nextView:DemoView)=>{
    setSelected(pkg);setView(nextView);setDevice("desktop");setDemoOpen(true);
  };

  return <main className={styles.page} dir="rtl">
    <header className={styles.header}>
      <div className={styles.headerInner}>
        <div className={styles.brand}><span>H</span><div><b>HAG Studio Portfolio</b><small>Interactive Work Showcase</small></div></div>
        <div className={styles.headerActions}><Button asChild variant="secondary"><Link to="/projects"><Store/> مشاريعنا</Link></Button><Button asChild variant="secondary"><Link to="/"><ArrowRight/> الموقع الرسمي</Link></Button><Button asChild><a href="https://wa.me/201066560638" target="_blank" rel="noreferrer"><MessageCircle/> ابدأ مشروعك</a></Button></div>
      </div>
    </header>

    <section className={styles.hero}>
      <div className={styles.heroGlow}/><div className={styles.container}><div className={styles.heroGrid}>
        <div className={styles.heroCopy}><div className={styles.eyebrow}><Sparkles/> REAL WORK. REAL BUSINESS VALUE.</div><h1>مش بنعرض Screenshots.<br/><em>بنخليك تجرّب مستوى الشغل.</em></h1><p>كل باقة تحت فيها Storefront وAdmin Panel تفاعليين فعليًا: منتجات حقيقية الشكل، صور، سلة، طلبات وإدارة بمستوى يزيد مع كل باقة.</p><div className={styles.heroActions}><Button size="lg" onClick={()=>document.getElementById("packages-demo")?.scrollIntoView({behavior:"smooth"})}>جرّب الباقات <ChevronLeft/></Button><Button size="lg" variant="outline" className={styles.heroOutline} onClick={()=>openDemo("business","admin")}>افتح نموذج الإدارة <LayoutDashboard/></Button></div></div>
        <div className={styles.valuePanel}><div className={styles.valueTop}><span>HAG STUDIO VALUE STACK</span><b>من أول المنتج لحد الإدارة والتقارير.</b></div><div className={styles.valueGrid}><div><Store/><b>Storefront</b><span>Brand-first UX</span></div><div><LayoutDashboard/><b>Admin</b><span>Real Control</span></div><div><Users/><b>CRM</b><span>Customer Flow</span></div><div><CreditCard/><b>Payments</b><span>Business Ready</span></div></div></div>
      </div><div className={styles.heroStats}><div><b>3 باقات</b><span>Mini / Smart / Smart Plus</span></div><div><b>Store + Admin</b><span>مش مجرد Landing Page</span></div><div><b>Responsive</b><span>Mobile + Windows</span></div><div><b>Interactive</b><span>Cart + Orders + Control</span></div></div></div>
    </section>

    <section className={styles.packagesSection} id="packages-demo"><div className={styles.container}><div className={styles.sectionHead}><div><span>INTERACTIVE PACKAGE LAB</span><h2>افتح الباقة وجربها كأنها مشروع شغال.</h2></div><p>Search، Cart، Order Flow، Dashboard، CRM، Stock، Payments — كل مستوى بيفتح أدوات أكتر بشكل واضح.</p></div>
      <div className={styles.packageGrid}>{Object.values(packageData).map(pkg=><article key={pkg.id} className={[styles.packageCard,styles[pkg.tone],selected===pkg.id?styles.selectedPackage:""].join(" ")}><div className={styles.packageTop}><div><small>{pkg.label}</small><h3>{pkg.name}</h3><em>{pkg.reference}</em></div><div className={styles.packagePrice}><b>{pkg.price}</b><span>EGP</span></div></div><p>{pkg.description}</p><div className={styles.packageHighlights}>{pkg.highlights.map(x=><span key={x}><CheckCircle2/>{x}</span>)}</div><PackageSnapshot pkg={pkg.id}/><div className={styles.packageActions}><button onClick={()=>openDemo(pkg.id,"store")}><Store/> افتح تجربة المتجر</button><button onClick={()=>openDemo(pkg.id,"admin")}><LayoutDashboard/> افتح تجربة الإدارة</button></div></article>)}</div>
    </div></section>

    <section className={styles.proofSection}><div className={styles.container}><div className={styles.proofGrid}><div><Grid2X2/><b>Design مختلف لكل نشاط</b><span>الهوية والـFlow بيتبنوا حول البراند.</span></div><div><Zap/><b>تفاعل مش Mockup</b><span>Search، Cart، Orders وإدارة حقيقية.</span></div><div><Warehouse/><b>تشغيل وإدارة</b><span>الموقع يخدم البزنس بعد النشر.</span></div><div><PackageCheck/><b>قابل للتوسع</b><span>من Mini لحد Smart Plus + Custom.</span></div></div></div></section>

    <section className={styles.cta}><div className={styles.container}><div className={styles.ctaCard}><div><span>READY TO BUILD?</span><h2>المشروع الجاي ممكن يبقى بتاعك.</h2><p>ابعتلنا النشاط والهدف، وإحنا نبني تجربة تناسب العميل والإدارة سوا.</p></div><Button asChild size="lg"><a href="https://wa.me/201066560638" target="_blank" rel="noreferrer"><MessageCircle/> ابدأ مشروعك</a></Button></div></div></section>

    {demoOpen&&<div className={styles.modalBackdrop} onClick={()=>setDemoOpen(false)}><section className={styles.demoModal} onClick={e=>e.stopPropagation()}>
      <div className={styles.modalHead}><div><span>INTERACTIVE PACKAGE EXPERIENCE</span><h2>{packageData[selected].name} — Store + Admin</h2><small>{packageData[selected].reference}</small></div><button onClick={()=>setDemoOpen(false)}><X/></button></div>
      <div className={styles.demoControls}><div className={styles.demoTabs}><button className={view==="store"?styles.demoTabActive:""} onClick={()=>setView("store")}><Store/> Storefront</button><button className={view==="admin"?styles.demoTabActive:""} onClick={()=>setView("admin")}><LayoutDashboard/> Admin Panel</button></div><div className={styles.deviceTabs}><button className={device==="desktop"?styles.deviceActive:""} onClick={()=>setDevice("desktop")}><Monitor/> Desktop</button><button className={device==="mobile"?styles.deviceActive:""} onClick={()=>setDevice("mobile")}><Smartphone/> Mobile</button></div></div>
      <div className={[styles.demoStage,device==="mobile"?styles.mobileStage:""].join(" ")}><div className={styles.demoDeviceFrame}>{view==="store"?<StoreDemo pkg={selected}/>:<AdminDemo pkg={selected}/>}</div></div>
      <div className={styles.modalFooter}><span>الديمو بيحاكي مستوى الشغل والـFlow. التصميم النهائي بيتخصص بالكامل حسب البراند والنشاط.</span><Button asChild><a href="https://wa.me/201066560638" target="_blank" rel="noreferrer">اسأل عن {packageData[selected].name}</a></Button></div>
    </section></div>}
  </main>
}
