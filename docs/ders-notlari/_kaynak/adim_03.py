"""Adım 3 ders notu: Frontend yükseltmesi."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfkit import build  # noqa: E402

M = lambda s: f"<font name='Mono'>{s}</font>"  # noqa: E731

B = [
    ("note", "Bu adımda ne değişti?",
     "Frontend'in tüm temelini bir yıl ileri taşıdık: Node 20 → 26, Vite 6 → 8, MUI 6 → 9, React Router 7 → 8, "
     "ESLint 9 → 10, TypeScript 5.7 → 6. Ardından eski kalıntıları temizledik ve fiyatları Türk lirası "
     "formatına geçirdik. Bu notta hem bu araçların <b>ne olduğunu</b>, hem de büyük bir bağımlılık "
     "yükseltmesinin <b>nasıl güvenle yapıldığını</b> anlatıyoruz."),

    # ------------------------------------------------------------------
    ("h1", "1. Frontend'in parçaları: kim ne iş yapıyor?"),
    ("flow", [
        ("Node.js + npm", "Araçları çalıştırır<br/>paketleri indirir"),
        ("Vite", "Geliştirme sunucusu<br/>ve derleyici"),
        ("Tarayıcı", "React + MUI<br/>+ Redux"),
        ("API", "RTK Query ile<br/>JSON alışverişi"),
    ]),
    ("table", [
        ["Araç", "Ne işe yarıyor?", "Ne zaman çalışıyor?"],
        ["<b>Node.js</b>", "JavaScript'i tarayıcı dışında çalıştıran motor. Vite, ESLint, TypeScript derleyicisi "
                           "Node üzerinde çalışır.", "Sadece geliştirirken (senin bilgisayarında)"],
        ["<b>npm</b>", "Node'un paket yöneticisi. NuGet'in JavaScript karşılığı.", "Paket kurarken, script çalıştırırken"],
        ["<b>Vite</b>", "Kodu tarayıcıya sunar, kaydettiğinde anında günceller, yayın için paketler.", "Geliştirme ve build"],
        ["<b>TypeScript</b>", "Kodu çalıştırmadan önce tip hatalarını bulur.", "Yazarken ve build sırasında"],
        ["<b>ESLint</b>", "Hatalı ya da riskli kod kalıplarını bulur (kurallar).", "Yazarken ve lint sırasında"],
        ["<b>React, MUI, Redux, Router</b>", "Uygulamanın kendisi. Tarayıcıya giden kod bunlar.", "Kullanıcının tarayıcısında"],
    ], [0.22, 0.50, 0.28]),
    ("tip", "Önemli ayrım",
     "Node.js kullanıcının bilgisayarına gitmez. Tarayıcı Node'u bilmez; Vite'ın ürettiği saf JavaScript, HTML ve "
     "CSS dosyalarını çalıştırır. Node sadece <b>geliştirme araçlarının</b> motorudur."),

    # ------------------------------------------------------------------
    ("h1", "2. Node.js ve npm"),
    ("h2", "Node'un sürüm döngüsü"),
    ("p", "Node.js her yıl iki ana sürüm çıkarır. <b>Çift numaralılar</b> (22, 24, 26) Ekim ayında <b>LTS</b> olur ve "
          "yaklaşık 2,5 yıl desteklenir; tek numaralılar (23, 25) kısa ömürlüdür. Biz <b>Node 26 LTS</b>'e geçtik. "
          "Node 20'nin desteği Nisan 2026'da bitmişti, ayrıca React Router 8 en az Node 22.22 istiyor."),
    ("p", "Bunu " + M("package.json") + "'a da yazdık. Projeyi klonlayan biri eski Node ile kurmaya çalışırsa uyarı alır:"),
    ("code", """"engines": {
  "node": ">=22.22.0"
}"""),
    ("warn", "Karşılaştığımız tuzak: Eski npm yenisinin önüne geçti",
     "Node 26 kurulduğu halde " + M("npm -v") + " 10.4 gösteriyordu. Geçmişte " + M("npm install -g npm") +
     " ile global bir npm kurulmuştu. Node'un " + M("npm.cmd") + " dosyası önce global npm var mı diye bakar, varsa "
     "<b>onu çalıştırır</b>. Çözüm: " + M("npm install -g npm@latest") + " ile global npm'i de güncellemek. "
     "İpucu: Hata mesajındaki büyük harfli " + M("npm ERR!") + " eski npm'in, küçük harfli " + M("npm error") +
     " yenisinin işaretidir."),

    ("h2", "package.json ve package-lock.json"),
    ("table", [
        ["", M("package.json"), M("package-lock.json")],
        ["Kim yazar", "Sen", "npm otomatik"],
        ["İçerik", "Hangi paketleri, hangi sürüm aralığında istediğin", "Kurulan <b>her</b> paketin (alt bağımlılıklar dahil) tam sürümü"],
        ["Örnek", M("\"vite\": \"^8.3.8\""), M("vite 8.3.8, rolldown 1.x.y, ...") + " yüzlerce satır"],
        ["Amaç", "Niyeti belirtmek", "Herkesin bilgisayarında <b>birebir aynı</b> ağacın kurulması"],
        ["Git'e", "Gider", "Gider (önemli!)"],
    ], [0.15, 0.40, 0.45]),
    ("h2", "Semver: sürüm numaraları ne anlatıyor?"),
    ("p", "<b>Semantic Versioning</b>: " + M("MAJOR.MINOR.PATCH") + " → " + M("8.3.8") + ". "
          "<b>PATCH</b> hata düzeltmesidir, <b>MINOR</b> geriye uyumlu yeni özelliktir, <b>MAJOR</b> ise "
          "<b>kırıcı değişiklik</b> (breaking change) demektir. Bu adımda yaptığımız şey, tam olarak bir sürü "
          "MAJOR atlamasıydı; bu yüzden kod değişikliği gerekti."),
    ("table", [
        ["Yazım", "Anlamı", "Örnek"],
        [M("^8.3.8"), "8.x.x içinde en yenisi; 9'a geçmez", "8.4.0 kurulabilir, 9.0.0 kurulmaz"],
        [M("~6.0.3"), "6.0.x içinde en yenisi; 6.1'e geçmez", "6.0.5 kurulabilir, 6.1.0 kurulmaz"],
        [M("8.3.8"), "Tam olarak bu sürüm", "Sadece 8.3.8"],
    ], [0.18, 0.47, 0.35]),
    ("p", "TypeScript için " + M("~") + " kullandık, çünkü " + M("typescript-eslint") + " sadece " +
          M("&lt;6.1") + " sürümlerini destekliyor. TypeScript 6.1 çıktığında kendiliğinden kurulup lint'i bozmasın."),

    ("h2", "dependencies, devDependencies ve peerDependencies"),
    ("terms", [
        ("dependencies", "Uygulamanın çalışması için gereken, tarayıcıya giden paketler: React, MUI, Redux."),
        ("devDependencies", "Sadece geliştirme ve build sırasında gereken araçlar: Vite, TypeScript, ESLint. "
                            "Kullanıcının tarayıcısına gitmez."),
        ("peerDependencies", "Bir paketin \"beni kullanan projede şu da olmalı\" demesi. Örneğin "
                             + M("@eslint/js@10") + " der ki: \"ESLint 10 ile çalışırım.\" Kendisi kurmaz, senden bekler."),
    ]),
    ("warn", "Karşılaştığımız hata: ERESOLVE",
     "Yeni " + M("@eslint/js@10") + " ESLint 10 istiyordu, ama eski " + M("package-lock.json") + " ESLint 9.22'yi "
     "kilitlemişti. npm ikisini birden sağlayamadığı için durdu. Çözüm: Büyük bir yükseltmede lock dosyasını ve "
     + M("node_modules") + "'u silip <b>sıfırdan</b> kurmak. Hata mesajı " + M("--force") + " ya da "
     + M("--legacy-peer-deps") + " önerir. <b>Bunları kullanma:</b> Çakışmayı çözmezler, gizlerler. Sonra çalışma "
     "anında açıklaması zor hatalar çıkar."),

    # ------------------------------------------------------------------
    ("h1", "3. Vite"),
    ("p", "<b>Vite</b> (Fransızca \"hızlı\") iki iş yapar:"),
    ("bullets", [
        "<b>Geliştirme sunucusu</b> (" + M("npm run dev") + "): Kodunu " + M("https://localhost:3000") + "'de sunar. "
        "Bir dosyayı kaydettiğinde sayfayı yenilemeden sadece değişen bileşeni günceller. Buna <b>HMR</b> "
        "(Hot Module Replacement) denir; form doldururken bile durumun kaybolmaz.",
        "<b>Build</b> (" + M("npm run build") + "): TypeScript ve JSX'i tarayıcının anladığı JavaScript'e çevirir, "
        "yüzlerce dosyayı birkaç küçük dosyada birleştirir (bundle), küçültür (minify) ve " + M("dist/") +
        " klasörüne yazar. Yayına giden şey bu klasördür.",
    ]),
    ("p", "Vite 8'in en büyük yeniliği, arka plandaki derleyicinin Rust ile yazılmış <b>Rolldown</b>'a geçmesi. "
          "Build'ler belirgin şekilde hızlandı. Bu yüzden Vite, " + M("@vitejs/plugin-react-swc") + " yerine "
          "Rolldown/Oxc ile çalışan " + M("@vitejs/plugin-react") + " kullanmamızı öneriyordu; biz de geçtik."),
    ("h2", "vite-plugin-mkcert: localhost'ta HTTPS"),
    ("p", "Bu eklenti bilgisayarına yerel bir sertifika otoritesi kurar ve " + M("localhost") + " için güvenilir bir "
          "HTTPS sertifikası üretir. Neden önemli? Adım 7'de giriş için <b>cookie</b> kullanacağız ve güvenli "
          "cookie'ler (" + M("Secure") + ") sadece HTTPS üzerinden gönderilir. Geliştirmede de production gibi "
          "HTTPS kullanmak sürprizleri önler."),
    ("h2", "Ortam değişkenleri: .env.development"),
    ("code", """# client/.env.development
VITE_API_URL=https://localhost:5001/api

// baseApi.ts
baseUrl: import.meta.env.VITE_API_URL,"""),
    ("bullets", [
        "Vite, " + M("npm run dev") + " sırasında " + M(".env.development") + "'ı, build sırasında "
        + M(".env.production") + "'ı okur. API adresi ortama göre değişir ama kod aynı kalır.",
        "Sadece <b>" + M("VITE_") + " ile başlayan</b> değişkenler tarayıcı koduna gömülür. Bu bir güvenlik önlemi: "
        "bilmeden bir sırrı tarayıcıya göndermeyesin diye.",
        M("import.meta.env.DEV") + " geliştirmede " + M("true") + ", build'de " + M("false") + " olur. "
        "Yapay bekletme gibi sadece geliştirmeye özel kodlar için kullanılır.",
    ]),
    ("warn", "Altın kural: Frontend'de sır olmaz",
     "Tarayıcıya giden her şey (" + M("VITE_") + " değişkenleri dahil) kullanıcının görebileceği koddadır. "
     "iyzico secret key'i, Cloudinary API secret'ı gibi bilgiler <b>sadece backend'de</b> durur. Frontend'e "
     "en fazla \"public\" anahtarlar konabilir."),

    # ------------------------------------------------------------------
    ("h1", "4. TypeScript: hem güvenlik ağı hem yükseltme aracı"),
    ("p", M("npx tsc -b") + " tüm projeyi tip açısından kontrol eder. Yükseltmeden sonra çalıştırdığımızda "
          "bozulan <b>her yeri</b> dosya ve satır numarasıyla verdi: 6 dosyada " + M("react-router-dom") +
          " bulunamadı, " + M("Grid2") + " yok, " + M("Box") + "'ta " + M("display") + " prop'u yok. Kütüphane "
          "dokümanındaki \"breaking changes\" listesini satır satır okumak yerine derleyiciyi bir yapılacaklar "
          "listesi gibi kullandık. Tipli dil kullanmanın en büyük faydalarından biri bu."),
    ("h2", "Neden TypeScript 7 değil?"),
    ("p", "TypeScript 7, derleyicinin Go diliyle baştan yazılmış hali ve yaklaşık 10 kat daha hızlı. Ama ekosistem "
          "henüz yetişmedi: " + M("typescript-eslint") + "'in son sürümü TypeScript'i " + M("&gt;=4.8.4 &lt;6.1.0") +
          " aralığında destekliyor. TS 7 kursaydık lint çalışmazdı. Bunu " + M("npm view typescript-eslint peerDependencies") +
          " komutuyla kontrol ettik. Ders: Büyük bir sürüm çıktığında, ona bağımlı araçların da desteklediğinden emin ol."),
    ("warn", "Karşılaştığımız tuzak: TypeScript her hatayı yakalamaz",
     M("sx={{ mw: \"lg\" }}") + " yazıldığında derleyici hata vermedi, ama MUI'de " + M("mw") + " diye bir kısaltma yok "
     "(" + M("mt") + ", " + M("mx") + ", " + M("p") + " var ama " + M("maxWidth") + "'in kısaltması yok). Stil sessizce "
     "uygulanmadı. " + M("sx") + " nesnesi serbest CSS anahtarlarını da kabul ettiği için TypeScript bunu yanlış "
     "bulmaz. Ders: Build'in geçmesi \"her şey doğru\" demek değildir; değişikliği <b>ekranda da</b> kontrol et."),

    # ------------------------------------------------------------------
    ("h1", "5. ESLint ve yeni \"flat config\""),
    ("p", "<b>ESLint</b>, kodu çalıştırmadan okuyup kurallara göre sorunları bulan bir araçtır (<b>linter</b>). "
          "TypeScript tipleri kontrol eder, ESLint ise kalıpları: kullanılmayan değişken, " + M("useEffect") +
          " içinde eksik bağımlılık, hook'un koşul içinde çağrılması gibi."),
    ("code", """export default defineConfig([
  globalIgnores(["dist"]),                       // build çıktısını kontrol etme
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,                    // temel JavaScript kuralları
      tseslint.configs.recommended,              // TypeScript kuralları
      reactHooks.configs.flat.recommended,       // React hook kuralları
      reactRefresh.configs.vite,                 // HMR'ın düzgün çalışması için
    ],
    languageOptions: { globals: globals.browser },
  },
]);"""),
    ("p", M("defineConfig") + " ESLint'in kendi fonksiyonu; " + M("typescript-eslint") + "'in eski " + M("tseslint.config") +
          " yardımcısının yerini aldı. " + M("extends") + " ile hazır kural setlerini üst üste koyuyoruz. "
          + M("eslint-plugin-react-hooks") + " 7. sürümle birlikte React Compiler'ın kurallarını da içeriyor."),

    # ------------------------------------------------------------------
    ("h1", "6. React Router 8"),
    ("p", "<b>React Router</b>, URL'ye göre hangi bileşenin gösterileceğine karar verir. SPA'da sayfa hiç yenilenmez; "
          "Router, adres çubuğunu değiştirip doğru bileşeni çizer."),
    ("code", """createBrowserRouter([
  {
    path: "/",
    element: <App />,                 // her sayfada görünen çerçeve (NavBar + Outlet)
    children: [
      { path: "/catalog", element: <Catalog /> },
      { path: "/catalog/:id", element: <ProductDetails /> },  // :id → useParams()
    ],
  },
]);"""),
    ("terms", [
        ("Nested route", "İç içe rota. " + M("App") + " her sayfada sabit kalır, " + M("children") + " değişir."),
        ("Outlet", M("App") + " içinde, o anki alt sayfanın çizileceği yer."),
        ("useParams", "URL'deki parametreyi okur: " + M("/catalog/5") + " → " + M("{ id: \"5\" }") + "."),
        ("Link / NavLink", "Sayfayı yenilemeden gezinmeyi sağlayan bağlantı. " + M("NavLink") + " aktif sayfaya "
                           + M("active") + " sınıfı ekler (menüde vurgulama için)."),
    ]),
    ("p", "v8'deki ana değişiklik: Eskiden iki paket vardı (" + M("react-router") + " çekirdek, " + M("react-router-dom") +
          " tarayıcı). Artık tek paket var: " + M("react-router") + ". Tarayıcıya özel birkaç API (örneğin "
          + M("RouterProvider") + "'ın DOM versiyonu) " + M("react-router/dom") + " altından gelir. Kırıcı "
          "değişiklikler az, çünkü ekip bunları v7'de \"future flag\" olarak önceden sundu."),

    # ------------------------------------------------------------------
    ("h1", "7. MUI 9 ve sx prop'u"),
    ("p", "<b>MUI</b> (Material UI), Google'ın Material Design kurallarına göre hazırlanmış React bileşen kütüphanesidir. "
          "Buton, kart, tablo, menü gibi bileşenleri hazır ve erişilebilir (klavye, ekran okuyucu) şekilde verir."),
    ("h2", "System props kaldırıldı, her şey sx'te"),
    ("code", """// MUI 6 (artık geçersiz)
<Box display="flex" alignItems="center" mt={2}>

// MUI 9
<Box sx={{ display: "flex", alignItems: "center", mt: 2 }}>"""),
    ("p", "Neden? Aynı işi yapan iki yol vardı, ve her bileşenin onlarca stil prop'unu ayrıca tanıması hem kütüphaneyi "
          "büyütüyor hem de TypeScript'i yavaşlatıyordu. Artık tek kural var: <b>stil " + M("sx") + "'e, davranış "
          "prop'lara</b>. " + M("sx") + " içinde tema değerlerini kısaltmalarla kullanabilirsin: " + M("mt: 2") +
          " = " + M("theme.spacing(2)") + " = 16px, " + M("color: \"secondary.main\"") + " = temadaki ikincil renk."),
    ("h2", "Grid"),
    ("p", "Eski " + M("Grid") + " kaldırıldı, MUI 6'daki " + M("Grid2") + " artık " + M("Grid") + " adını aldı. "
          "Grid sayfayı <b>12 sütuna</b> böler: " + M("size={6}") + " yarım genişlik demek. Ekrana göre değiştirmek "
          "için " + M("size={{ xs: 12, md: 6 }}") + " yazılır: telefonda tam, masaüstünde yarım genişlik."),

    # ------------------------------------------------------------------
    ("h1", "8. Redux Toolkit ve RTK Query"),
    ("p", "Redux, uygulama genelinde paylaşılan durumu (state) <b>tek bir merkezde</b> (store) tutar. Dark mode "
          "tercihi, yükleniyor çubuğu, ileride sepet ve giriş yapmış kullanıcı burada duracak. Herhangi bir bileşen "
          "bu durumu okuyabilir ve değiştirmek için bir <b>action</b> gönderebilir."),
    ("terms", [
        ("Store", "Tüm uygulama durumunun tutulduğu tek nesne. " + M("configureStore") + " ile oluşturulur."),
        ("Slice", "Durumun bir parçası ve onu değiştiren fonksiyonlar. Bizde " + M("uiSlice") + ": " +
                  M("isLoading") + ", " + M("darkMode") + "."),
        ("Reducer", "\"Mevcut durum + action → yeni durum\" hesaplayan fonksiyon. " + M("createSlice") +
                    " sayede sanki doğrudan değiştiriyormuş gibi yazabiliyoruz (" + M("state.darkMode = ...") + "); "
                    "arka planda Immer kütüphanesi yeni bir kopya üretir."),
        ("Action / dispatch", M("dispatch(setDarkMode())") + " → \"dark mode'u değiştir\" mesajını store'a gönder."),
        ("Selector", M("useAppSelector(state => state.ui)") + " → store'dan ihtiyacın olan parçayı oku."),
        ("Middleware", "Action'ların arasına giren ek işlem katmanı. RTK Query'nin önbelleği ve istek yönetimi bir middleware."),
    ]),
    ("h2", "RTK Query"),
    ("p", "API'den veri çekmeyi tamamen üstlenen Redux Toolkit modülü. " + M("createApi") + " ile endpoint'leri "
          "tanımlıyoruz, o da bize hazır hook'lar üretiyor:"),
    ("code", """const { data, isLoading } = useFetchProductsQuery();"""),
    ("bullets", [
        "<b>Önbellek (cache):</b> Katalogdan detaya gidip geri döndüğünde ürünler tekrar indirilmez.",
        "<b>Durumlar hazır:</b> " + M("isLoading") + ", " + M("isError") + ", " + M("data") + " ile " +
        M("useState") + " ve " + M("useEffect") + " yazmaya gerek kalmaz.",
        "<b>Ortak baseQuery:</b> " + M("baseQueryWithErrorHandling") + " her isteğin etrafına yükleniyor çubuğu ve "
        "hata kaydı ekliyor. Adım 4'te hata yönetimini buraya kuracağız.",
    ]),
    ("p", "Temizlikte " + M("redux") + " paketini ve " + M("legacy_createStore") + "'u kaldırdık. Redux Toolkit, redux'u "
          "zaten içinde getiriyor; " + M("legacy_createStore") + " ise eski tarz Redux'tu, kurs sırasında karşılaştırma "
          "için yazılmıştı."),

    # ------------------------------------------------------------------
    ("h1", "9. Para gösterimi: Intl.NumberFormat"),
    ("code", """const tryFormatter = new Intl.NumberFormat("tr-TR", { style: "currency", currency: "TRY" });

export function formatCurrency(kurus: number) {
  return tryFormatter.format(kurus / 100);   // 20000 → "₺200,00"
}"""),
    ("bullets", [
        M("Intl") + ", tarayıcıya gömülü uluslararasılaştırma (internationalization) API'si. Para, tarih, sayı "
        "formatlarını dile ve ülkeye göre doğru yazar: " + M("tr-TR") + " → ondalık ayırıcı virgül, binlik ayırıcı nokta.",
        "Formatter'ı fonksiyonun <b>dışında</b> bir kere oluşturduk; her çağrıda yeniden oluşturmak gereksiz maliyet.",
        "Fiyat backend'de kuruş olarak tutuluyor, " + M("/ 100") + " işlemi sadece ekranda yapılıyor.",
        "Tüm formatlama tek bir fonksiyonda; para birimi değişirse tek bir yeri değiştireceğiz. "
        "Buna <b>DRY</b> (Don't Repeat Yourself) prensibi denir.",
    ]),

    # ------------------------------------------------------------------
    ("h1", "10. Büyük bir yükseltme nasıl güvenle yapılır?"),
    ("steps", [
        "<b>Güncel durumu gör:</b> " + M("npm outdated") + " hangi paketin ne kadar geride olduğunu listeler.",
        "<b>Uyumluluğu kontrol et:</b> " + M("npm view &lt;paket&gt; engines peerDependencies") + " ile her paketin "
        "hangi Node ve hangi kardeş paketleri istediğine bak.",
        "<b>Migration rehberlerini oku:</b> Her MAJOR sürümün \"upgrade guide\" sayfası var.",
        "<b>Önce bir kopyada dene:</b> Biz yükseltmeyi önce geçici bir kopyada denedik; ERESOLVE ve SWC uyarısı orada çıktı.",
        "<b>Sıfırdan kur:</b> Lock dosyası ve node_modules silinip temiz kurulum.",
        "<b>Derleyiciyi kullan:</b> " + M("npx tsc -b") + " bozulan her yeri listeler.",
        "<b>Lint + build + ekranda test:</b> Üçü de geçmeden commit yok.",
    ]),

    ("h1", "11. Bu adımda ne yaptık?"),
    ("steps", [
        "Node 26 LTS kuruldu, global npm güncellendi.",
        M("package.json") + " yeni sürümlere çekildi, " + M("engines") + " eklendi, " + M("redux") + " ve "
        + M("react-router-dom") + " kaldırıldı, lock dosyası sıfırdan oluştu.",
        "Vite eklentisi " + M("plugin-react") + "'e geçti, ESLint " + M("defineConfig") + " formatına çevrildi.",
        "6 dosyada " + M("react-router") + " import'ları, MUI system props → " + M("sx") + ", " + M("Grid2") + " → " + M("Grid") + ".",
        "Counter demosu ve " + M("legacy_createStore") + " kaldırıldı, ContactPage sadeleşti.",
        "API adresi " + M(".env.development") + " dosyasına taşındı.",
        M("formatCurrency") + " ile fiyatlar ₺ formatında.",
    ]),

    ("h1", "12. Sözlük"),
    ("terms", [
        ("LTS", "Uzun süreli destek alan sürüm. Node'da çift numaralılar."),
        ("Semver", "MAJOR.MINOR.PATCH sürümleme kuralı. MAJOR artışı kırıcı değişiklik demektir."),
        ("Breaking change", "Eski kodun çalışmasını bozan değişiklik."),
        ("Lock file", "Kurulan tüm paketlerin tam sürümlerini sabitleyen dosya."),
        ("Peer dependency", "Bir paketin, kendisini kullanan projeden beklediği kardeş paket."),
        ("Bundle", "Birçok kaynak dosyanın tarayıcı için birleştirilmiş hali."),
        ("HMR", "Sayfayı yenilemeden sadece değişen modülü güncelleme."),
        ("Linter", "Kodu çalıştırmadan okuyup kurallara göre sorun bulan araç (ESLint)."),
        ("SPA", "Tek HTML sayfası üzerinde, yenilenmeden içeriği değişen uygulama."),
        ("Store / Slice", "Redux'ta tüm durum / durumun bir parçası ve onu değiştiren fonksiyonlar."),
        ("Cache", "Daha önce alınmış verinin tekrar istenmeden kullanılmak üzere saklanması."),
        ("sx prop", "MUI bileşenlerine tema değerleriyle stil vermenin tek yolu."),
        ("Intl", "Tarayıcının dil ve ülkeye göre biçimlendirme API'si."),
        ("DRY", "Aynı bilgiyi ya da mantığı tek bir yerde tut prensibi."),
    ]),

    ("h1", "13. Kendini test et"),
    ("steps", [
        "Node.js kullanıcının tarayıcısında çalışıyor mu? Neden ihtiyacımız var?",
        M("package.json") + " ile " + M("package-lock.json") + " arasındaki fark ne? Lock dosyası neden git'e gider?",
        M("^8.3.8") + " ile " + M("~6.0.3") + " ne anlama geliyor? TypeScript için neden " + M("~") + " seçtik?",
        "ERESOLVE hatası ne demek? Neden " + M("--force") + " ile geçmedik?",
        "Node 26 kurduğumuz halde neden npm 10 çalışıyordu?",
        M(".env.development") + "'a iyzico secret key'i yazabilir miyiz? Neden?",
        "TypeScript 7 varken neden 6 kurduk?",
        M("sx={{ mw: \"lg\" }}") + " neden derleme hatası vermedi? Bundan ne ders çıkardık?",
        "MUI 9'da " + M("&lt;Box mt={2}&gt;") + " neden artık çalışmıyor? Doğrusu ne?",
        "RTK Query olmasaydı ürün listesini çekmek için hangi React hook'larını yazmamız gerekirdi?",
        M("formatCurrency") + " içindeki formatter'ı neden fonksiyonun dışında oluşturduk?",
    ]),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "Adim-03-Frontend-Yukseltmesi.pdf")
    build(os.path.abspath(out),
          "Adım 3: Frontend Yükseltmesi",
          "Node 26, npm ve semver, Vite 8, TypeScript 6, ESLint 10, React Router 8, MUI 9, Redux Toolkit, Intl",
          B, "E-Commerce Projesi · Ders Notları · Adım 3")
    print("ok", os.path.abspath(out))
