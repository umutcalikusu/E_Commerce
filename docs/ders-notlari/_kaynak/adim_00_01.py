"""Adım 0 ve Adım 1 ders notu: .NET 11 yükseltmesi ve Docker ortamı."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfkit import build  # noqa: E402

B = [
    ("note", "Bu notlar ne için?",
     "Her adımın sonunda, o adımda kullandığımız teknolojilerin <b>ne olduğunu</b>, "
     "<b>ne işe yaradığını</b> ve <b>neden seçtiğimizi</b> buraya yazıyoruz. Amaç, "
     "bir mülakatta ya da bir müşteriye \"neden Docker kullandın?\" diye sorulduğunda "
     "rahatça cevap verebilmen. Sondaki sözlük ve \"kendini test et\" soruları tekrar için."),

    # ------------------------------------------------------------------
    ("h1", "1. Büyük resim: Uygulamamız nasıl çalışıyor?"),
    ("p", "Projemiz iki ayrı uygulamadan oluşuyor ve bunlar birbiriyle internet üzerinden "
          "(HTTP) konuşuyor. Bu yapıya <b>client-server (istemci-sunucu)</b> mimarisi denir."),
    ("flow", [
        ("Tarayıcı", "React uygulaması<br/>localhost:3000"),
        ("API", "ASP.NET Core<br/>localhost:5001"),
        ("EF Core", "C# nesnesi ↔ SQL"),
        ("PostgreSQL", "Docker içinde<br/>localhost:5433"),
    ]),
    ("bullets", [
        "<b>Client (istemci):</b> Kullanıcının gördüğü taraf. Bizde <b>React</b> ile yazılmış, "
        "tarayıcıda çalışan bir <b>SPA</b> (Single Page Application: sayfa yenilenmeden içeriği "
        "değişen uygulama).",
        "<b>Server (sunucu):</b> İş kurallarının ve verinin olduğu taraf. Bizde <b>ASP.NET Core Web API</b>. "
        "Ekran çizmez, sadece JSON veri döndürür.",
        "<b>Veritabanı:</b> Verinin kalıcı olarak saklandığı yer. Artık <b>PostgreSQL</b>, ve Docker "
        "içinde çalışıyor.",
    ]),
    ("p", "Örnek akış: Kullanıcı katalog sayfasını açar → React, <font name='Mono'>GET /api/products</font> "
          "isteği atar → API'deki <font name='Mono'>ProductsController</font> isteği karşılar → EF Core "
          "veritabanına SQL sorgusu gönderir → gelen satırlar C# nesnesine, oradan JSON'a çevrilir → "
          "React bu JSON'u ekrana kart olarak çizer."),
    ("tip", "Neden iki ayrı uygulama?",
     "Frontend ve backend ayrı olunca aynı API'yi ileride bir mobil uygulama da kullanabilir; "
     "iki taraf bağımsız geliştirilip bağımsız yayınlanabilir. Freelance işlerde en çok istenen yapı budur."),

    # ------------------------------------------------------------------
    ("h1", "2. .NET nedir?"),
    ("p", "<b>.NET</b>, Microsoft'un açık kaynaklı, Windows/Linux/macOS'ta çalışan yazılım geliştirme "
          "platformudur. Biz backend'i .NET üzerinde <b>C#</b> diliyle yazıyoruz. Üç kavramı ayırmak önemli:"),
    ("table", [
        ["Kavram", "Ne demek?", "Bizim projede"],
        ["<b>Runtime</b>", "Derlenmiş programı çalıştıran motor. Sadece çalıştırmak isteyen bilgisayarda bulunması yeterli.",
         "Sunucuda API'yi çalıştıran kısım"],
        ["<b>SDK</b>", "Runtime + derleyici + <font name='Mono'>dotnet</font> komut satırı aracı. Kod yazan kişide olmalı.",
         "Kurduğumuz <b>11.0.100</b>"],
        ["<b>C#</b>", "Programlama dili. Her .NET sürümüyle yeni bir C# sürümü gelir.",
         ".NET 11 ile <b>C# 15</b>"],
    ], [0.17, 0.53, 0.30]),

    ("h2", "LTS ve STS nedir? Neden .NET 11?"),
    ("p", "Microsoft her Kasım ayında yeni bir .NET sürümü çıkarır. <b>Çift numaralılar LTS</b> "
          "(Long Term Support: 3 yıl destek), <b>tek numaralılar STS</b> (Standard Term Support: 2 yıl destek) "
          "olur. \"Destek\" demek, o sürüme güvenlik yaması gelmeye devam etmesi demektir."),
    ("table", [
        ["Sürüm", "Tür", "Çıkış", "Destek bitişi"],
        [".NET 9", "STS", "Kasım 2024", "Kasım 2026 (bitti, bu yüzden yükselttik)"],
        [".NET 10", "LTS", "Kasım 2025", "Kasım 2028"],
        [".NET 11", "STS", "Kasım 2026", "Kasım 2028"],
    ], [0.18, 0.14, 0.22, 0.46]),
    ("p", "Gördüğün gibi .NET 10 ve .NET 11'in desteği aynı tarihte bitiyor. Bu yüzden en yeni "
          "özellikleri alıp hiçbir şey kaybetmediğimiz için .NET 11'i seçtik."),

    ("h2", ".csproj dosyası ve TargetFramework"),
    ("p", "<font name='Mono'>API.csproj</font> projenin kimlik kartıdır: hangi .NET sürümünü hedeflediği, "
          "hangi paketleri kullandığı burada yazar. Yaptığımız değişiklik:"),
    ("code", """<TargetFramework>net11.0</TargetFramework>   <!-- eskiden net9.0 -->
<Nullable>enable</Nullable>                   <!-- null olabilecek değişkenler için uyarı ver -->
<ImplicitUsings>enable</ImplicitUsings>       <!-- sık kullanılan using'leri otomatik ekle -->"""),

    ("h2", "NuGet paketleri"),
    ("p", "<b>NuGet</b>, .NET'in paket yöneticisidir (JavaScript'teki npm'in karşılığı). Başkalarının "
          "yazdığı hazır kütüphaneleri projemize ekler. <font name='Mono'>dotnet add package X</font> "
          "komutu csproj'a bir <font name='Mono'>PackageReference</font> satırı ekler. EF Core paketlerini "
          "<b>9.0.3</b>'ten <b>11.0.0</b>'a yükselttik, çünkü paket sürümleri genelde .NET sürümüyle aynı ilerler."),
    ("warn", "Karşılaştığımız güvenlik uyarısı: NU1903",
     "Derlemede <font name='Mono'>SQLitePCLRaw.lib.e_sqlite3 2.1.10</font> paketinde yüksek önemde bir güvenlik "
     "açığı olduğu yazdı. NuGet, kullandığın paketleri bilinen açıklar listesiyle (GitHub Advisory) "
     "karşılaştırır. Bu uyarıları görmezden gelme: çözüm çoğu zaman paketi güncellemektir. "
     "Bizde SQLite'tan PostgreSQL'e geçeceğimiz için bu paket tamamen kalkacak."),

    ("h2", "Solution: .sln yerine .slnx"),
    ("p", "<b>Solution</b>, birden çok projeyi (API, ileride Domain, Application, Infrastructure...) bir arada "
          "tutan çatıdır. Eski <font name='Mono'>.sln</font> formatı okunması zor, GUID dolu bir dosyaydı. "
          "Yeni <font name='Mono'>.slnx</font> sade bir XML dosyasıdır; git'te değişiklikleri okumak ve "
          "birleştirmek (merge) çok daha kolaydır. <font name='Mono'>dotnet sln migrate</font> ile çevirdik."),
    ("warn", "Karşılaştığımız hata: NETSDK1045",
     "Visual Studio 2022 .NET 11'i hedefleyemediği için \"The current .NET SDK does not support targeting .NET 11.0\" "
     "hatası verdi. SDK aslında kuruluydu, komut satırından <font name='Mono'>dotnet build</font> çalışıyordu. "
     "Sorun IDE'nin eski olmasıydı; <b>Visual Studio 2026</b> kurarak çözdük. Ders: Hata IDE'de çıkıyorsa "
     "önce komut satırında dene, sorunun koddan mı araçtan mı kaynaklandığını böyle ayırırsın."),

    # ------------------------------------------------------------------
    ("h1", "3. ASP.NET Core Web API"),
    ("p", "<b>ASP.NET Core</b>, .NET üzerinde web uygulaması ve API yazmak için kullanılan çatıdır (framework). "
          "<b>Web API</b> ise HTTP istekleri alıp JSON döndüren bir sunucu uygulamasıdır. Projede gördüğün "
          "parçalar:"),
    ("terms", [
        ("Program.cs", "Uygulamanın başlangıç noktası. İki bölümü var: <b>servislerin kaydı</b> "
                       "(<font name='Mono'>builder.Services.Add...</font>) ve <b>pipeline</b> "
                       "(<font name='Mono'>app.Use...</font> / <font name='Mono'>app.Map...</font>)."),
        ("Controller", "İstekleri karşılayan sınıf. <font name='Mono'>[Route(\"api/[controller]\")]</font> sayesinde "
                       "<font name='Mono'>ProductsController</font> → <font name='Mono'>/api/products</font> adresine bağlanır."),
        ("HTTP metodları", "<b>GET</b> veri okur, <b>POST</b> oluşturur, <b>PUT</b> günceller, <b>DELETE</b> siler. "
                           "<font name='Mono'>[HttpGet(\"{id}\")]</font> → <font name='Mono'>/api/products/5</font>."),
        ("Status code", "Cevabın sonucu: <b>200</b> OK, <b>201</b> oluşturuldu, <b>400</b> hatalı istek, "
                        "<b>401</b> giriş yapılmamış, <b>404</b> bulunamadı, <b>500</b> sunucu hatası."),
        ("Middleware", "Her isteğin sırayla içinden geçtiği ara katmanlar zinciri (pipeline). CORS, kimlik "
                       "doğrulama, hata yakalama birer middleware'dir. <b>Sıraları önemlidir.</b>"),
        ("CORS", "Tarayıcı güvenlik kuralı: <font name='Mono'>localhost:3000</font>'deki sayfa, "
                 "<font name='Mono'>localhost:5001</font>'e istek atabilmek için API'nin izin vermesi gerekir. "
                 "<font name='Mono'>WithOrigins(\"https://localhost:3000\")</font> bu izni veriyor."),
    ]),

    ("h2", "Dependency Injection (DI)"),
    ("p", "Controller'ımız veritabanına erişmek için <font name='Mono'>StoreContext</font>'e ihtiyaç duyuyor ama onu "
          "kendisi <font name='Mono'>new</font> ile oluşturmuyor. Bunun yerine ihtiyacını constructor'da "
          "<b>ister</b>, ASP.NET Core da hazır olanı <b>verir</b>. Buna <b>Dependency Injection</b> denir."),
    ("code", """// Program.cs: "StoreContext isteyen olursa, şu ayarlarla oluşturup ver"
builder.Services.AddDbContext<StoreContext>(opt => opt.UseSqlite(...));

// ProductsController.cs: primary constructor ile "bana StoreContext lazım"
public class ProductsController(StoreContext context) : ControllerBase"""),
    ("p", "<b>Neden önemli?</b> Sınıflar birbirine sıkı bağlı olmaz. Yarın SQLite yerine PostgreSQL kullanmak "
          "için controller'a dokunmadan sadece Program.cs'teki tek satırı değiştiririz. Test yazarken de "
          "gerçek veritabanı yerine sahtesini verebiliriz. Clean Architecture'ın temeli de bu fikirdir."),

    # ------------------------------------------------------------------
    ("h1", "4. Entity Framework Core (EF Core)"),
    ("p", "<b>EF Core</b>, Microsoft'un <b>ORM</b> (Object-Relational Mapper) kütüphanesidir. Veritabanı "
          "tablolar ve satırlarla, C# ise sınıflar ve nesnelerle çalışır. ORM bu iki dünya arasında "
          "<b>tercümanlık</b> yapar: SQL yazmadan C# kodu ile veritabanını yönetiriz."),
    ("code", """// Biz bunu yazarız:
var product = await context.Products.FindAsync(id);

// EF Core bunu üretip veritabanına gönderir:
SELECT * FROM "Products" WHERE "Id" = @id LIMIT 1"""),
    ("terms", [
        ("Entity", "Veritabanındaki bir tabloya karşılık gelen C# sınıfı. <font name='Mono'>Product</font> → "
                   "<font name='Mono'>Products</font> tablosu, her property bir kolon."),
        ("DbContext", "Veritabanıyla konuşan ana sınıf. Bizde <font name='Mono'>StoreContext</font>. "
                      "Bağlantıyı yönetir, değişiklikleri takip eder, <font name='Mono'>SaveChanges</font> ile kaydeder."),
        ("DbSet&lt;T&gt;", "Bir tabloyu temsil eder. <font name='Mono'>context.Products</font> üzerinden sorgu yazılır."),
        ("Provider", "EF Core'un hangi veritabanıyla konuşacağını belirleyen paket. Şu an "
                     "<font name='Mono'>Sqlite</font>; Adım 2'de <font name='Mono'>Npgsql</font> (PostgreSQL) olacak."),
        ("Migration", "Entity'lerdeki değişikliği veritabanına uygulayan, kod olarak saklanan \"şema değişiklik "
                      "dosyası\". Veritabanının git geçmişi gibi düşün. <font name='Mono'>dotnet ef migrations add X</font> "
                      "ile oluşturulur, <font name='Mono'>Database.Migrate()</font> ile uygulanır."),
        ("Seed", "Boş veritabanına başlangıç verisi eklemek. <font name='Mono'>DbInitializer</font> tablo boşsa "
                 "18 ürünü ekliyor."),
        ("dotnet-ef", "Migration komutlarını çalıştıran komut satırı aracı. Global kurulu, "
                      "<font name='Mono'>dotnet tool update --global dotnet-ef</font> ile 11'e güncelledik."),
    ]),
    ("tip", "Fiyatı neden kuruş olarak (long) tutuyoruz?",
     "<font name='Mono'>Price = 20000</font> aslında 200,00 TL demek. Ondalıklı sayılar (float/double) bilgisayarda "
     "tam olarak saklanamaz: 0.1 + 0.2 = 0.30000000000000004 olur. Parada bu kabul edilemez. Tam sayı "
     "(kuruş) ile çalışıp sadece ekranda 100'e bölmek, ödeme sistemlerinde standart bir yöntemdir."),

    # ------------------------------------------------------------------
    ("h1", "5. Frontend teknolojileri (kısa özet)"),
    ("p", "Frontend'i Adım 3'te yükselteceğiz; o adımın notunda detaylı anlatacağız. Şimdilik ne olduklarını bil:"),
    ("table", [
        ["Teknoloji", "Ne işe yarıyor?"],
        ["<b>React 19</b>", "Arayüzü küçük, tekrar kullanılabilir <b>bileşenlerden</b> (component) kurmaya yarayan kütüphane."],
        ["<b>TypeScript</b>", "Tipli JavaScript. <font name='Mono'>Product</font> tipinde <font name='Mono'>price</font> yerine "
                              "<font name='Mono'>prise</font> yazarsan daha çalıştırmadan hata verir."],
        ["<b>Vite</b>", "Geliştirme sunucusu ve derleme aracı. Kaydettiğin anda tarayıcıyı günceller."],
        ["<b>MUI</b>", "Hazır, şık arayüz bileşenleri (buton, tablo, kart...) sunan Material Design kütüphanesi."],
        ["<b>Redux Toolkit</b>", "Uygulama genelindeki durumu (dark mode, sepet, kullanıcı) tek merkezde tutar."],
        ["<b>RTK Query</b>", "API'den veri çekme, önbellekleme (cache) ve yükleniyor durumlarını otomatik yönetir."],
        ["<b>React Router</b>", "URL'ye göre hangi sayfanın gösterileceğini belirler (/catalog, /catalog/5...)."],
    ], [0.22, 0.78]),

    # ------------------------------------------------------------------
    ("h1", "6. Git ve .gitignore"),
    ("p", "<b>Git</b>, kodun sürüm geçmişini tutar. Her <b>commit</b> projenin o anki fotoğrafıdır; bir şey bozulursa "
          "eski commit'e dönebilirsin. Bu yüzden her adımı ayrı commit'le kaydediyoruz."),
    ("p", "<b>.gitignore</b>, git'in takip etmemesi gereken dosyaların listesidir:"),
    ("bullets", [
        "<b>Derleme çıktıları</b> (<font name='Mono'>bin/</font>, <font name='Mono'>obj/</font>, "
        "<font name='Mono'>node_modules/</font>): Kaynak koddan yeniden üretilebilir, gereksiz yer kaplar.",
        "<b>Kişisel ayarlar</b> (<font name='Mono'>.vs/</font>): Senin IDE'ne özel.",
        "<b>Geçici veritabanı dosyaları</b> (<font name='Mono'>*.db-shm</font>, <font name='Mono'>*.db-wal</font>): "
        "SQLite'ın çalışırken açtığı yardımcı dosyalar.",
        "<b>Gizli bilgiler</b> (<font name='Mono'>.env</font>): Şifreler. <b>En kritik madde budur.</b>",
    ]),
    ("warn", "Altın kural: Şifre asla GitHub'a gitmez",
     "Public bir repoya yüklenen şifre, botlar tarafından dakikalar içinde bulunur. Commit'ten sonra silsen bile "
     "git geçmişinde kalır. Bu yüzden commit'ten önce her zaman <font name='Mono'>git status</font> ile neyin "
     "gideceğine bak."),

    # ------------------------------------------------------------------
    ("h1", "7. Docker"),
    ("h2", "Hangi sorunu çözüyor?"),
    ("p", "Klasik senaryo: \"Benim bilgisayarımda çalışıyor ama seninkinde çalışmıyor.\" Sebebi farklı PostgreSQL "
          "sürümleri, farklı ayarlar, eksik kurulumlar. Bir freelance projeyi müşteriye teslim ettiğinde ya da "
          "GitHub'dan biri klonladığında, her şeyi elle kurmak zorunda kalması büyük sorun."),
    ("p", "<b>Docker</b>, bir yazılımı ihtiyaç duyduğu her şeyle (işletim sistemi parçaları, kütüphaneler, ayarlar) "
          "birlikte paketleyip <b>her bilgisayarda aynı şekilde</b> çalıştırmayı sağlar. Bilgisayarına PostgreSQL "
          "kurmadın; Docker hazır bir PostgreSQL paketini indirip izole bir kutuda çalıştırdı."),
    ("h2", "Temel kavramlar"),
    ("terms", [
        ("Image (imaj)", "Çalıştırılmaya hazır, salt-okunur paket. Bir <b>kalıp</b> ya da <b>tarif</b> gibi. "
                         "<font name='Mono'>postgres:18</font> bir image'dır; Docker Hub'dan indirilir."),
        ("Container", "Image'dan oluşturulmuş, <b>çalışan</b> kopya. Kalıptan çıkan kek gibi: aynı image'dan "
                      "istediğin kadar container çalıştırabilirsin. Bizde 3 container var."),
        ("Tag", "Image'ın sürümü. <font name='Mono'>postgres:18</font> → 18 sürümü. Tag yazmazsan "
                "<font name='Mono'>latest</font> gelir; bu yüzden veritabanında sürümü hep sabitliyoruz."),
        ("Volume", "Container'ın dışında, kalıcı veri alanı. Container silinince içindeki her şey silinir; "
                   "volume'deki veri kalır. Veritabanı dosyalarını <font name='Mono'>pgdata</font> volume'ünde tutuyoruz."),
        ("Port mapping", "<font name='Mono'>\"5433:5432\"</font> → <b>bilgisayarın:container'ın</b>. Senin "
                         "bilgisayarının 5433 portuna gelen bağlantı, container içindeki 5432'ye yönlendirilir."),
        ("Network", "Compose, servisler için ortak bir sanal ağ kurar. Bu ağın içinde servisler birbirine "
                    "<b>servis adıyla</b> ulaşır. pgAdmin'den bağlanırken host'a <font name='Mono'>postgres</font> "
                    "yazmamızın sebebi bu."),
        ("Docker Desktop", "Windows'ta Docker motorunu (engine) çalıştıran uygulama. Kapalıysa hiçbir container çalışmaz."),
    ]),
    ("tip", "Docker sanal makine (VM) değil",
     "Sanal makine koca bir işletim sistemini baştan sona çalıştırır (GB'larca RAM, dakikalarca açılış). "
     "Container ise ana sistemin çekirdeğini paylaşır, sadece uygulamayı izole eder: saniyeler içinde açılır, "
     "çok az kaynak harcar."),

    ("h2", "Docker Compose"),
    ("p", "Tek tek <font name='Mono'>docker run ...</font> komutları yazmak yerine, tüm servisleri ve ayarlarını tek "
          "bir <font name='Mono'>docker-compose.yml</font> dosyasında tanımlarız. Bu dosya projeyle birlikte git'e gider; "
          "böylece ortam da <b>kod olarak</b> saklanmış olur (Infrastructure as Code)."),
    ("table", [
        ["Satır", "Anlamı"],
        ["<font name='Mono'>image: postgres:18</font>", "Hangi image'dan container oluşturulacak."],
        ["<font name='Mono'>container_name</font>", "Container'a sabit, okunaklı bir isim verir."],
        ["<font name='Mono'>restart: unless-stopped</font>", "Docker yeniden başlarsa container'ı da başlat; sen durdurduysan başlatma."],
        ["<font name='Mono'>environment</font>", "Container'a verilen ayarlar (kullanıcı, şifre, veritabanı adı)."],
        ["<font name='Mono'>${POSTGRES_USER}</font>", "Değeri <font name='Mono'>.env</font> dosyasından oku. Şifre compose dosyasına yazılmaz."],
        ["<font name='Mono'>ports</font>", "Port yönlendirmesi (bilgisayar:container)."],
        ["<font name='Mono'>volumes</font>", "Kalıcı veri alanını container içindeki klasöre bağlar."],
        ["<font name='Mono'>healthcheck</font>", "Servis gerçekten hazır mı? <font name='Mono'>pg_isready</font> her 5 saniyede kontrol eder."],
        ["<font name='Mono'>depends_on ... service_healthy</font>", "pgAdmin, PostgreSQL sağlıklı olana kadar başlamasın."],
    ], [0.40, 0.60]),
    ("h2", "Sık kullanacağın komutlar"),
    ("code", """docker compose up -d        # tüm servisleri arka planda (-d: detached) başlat
docker compose ps           # durumlarını göster
docker compose logs -f postgres   # postgres'in loglarını canlı izle
docker compose stop         # durdur (veriler kalır)
docker compose down         # container'ları sil (volume'deki veriler kalır)
docker compose down -v      # DİKKAT: volume'ler de silinir, veritabanı sıfırlanır"""),

    ("h2", ".env ve .env.example"),
    ("p", "<font name='Mono'>.env</font> gerçek şifreleri tutar ve <b>git'e gitmez</b>. "
          "<font name='Mono'>.env.example</font> ise aynı anahtarları sahte değerlerle içerir ve <b>git'e gider</b>. "
          "Projeyi klonlayan kişi example'ı kopyalayıp kendi şifrelerini yazar. Böylece hangi ayarların "
          "gerektiğini bilir ama senin şifrelerini görmez."),

    # ------------------------------------------------------------------
    ("h1", "8. Servislerimiz"),
    ("h2", "PostgreSQL"),
    ("p", "Dünyanın en popüler açık kaynaklı, ücretsiz <b>ilişkisel veritabanlarından</b> biri. İlişkisel demek: veri "
          "tablolarda tutulur ve tablolar birbirine bağlanır (sipariş → kullanıcı, sipariş kalemi → ürün)."),
    ("table", [
        ["", "SQLite (eskiden)", "PostgreSQL (şimdi)"],
        ["Nasıl çalışır", "Tek bir dosya (store.db)", "Ayrı çalışan bir sunucu"],
        ["Aynı anda çok kullanıcı", "Zayıf; yazma işlemleri sıraya girer", "Güçlü; binlerce eş zamanlı bağlantı"],
        ["Gerçek projede", "Mobil uygulama, küçük araçlar", "E-ticaret, SaaS, kurumsal projeler"],
        ["Ücret", "Ücretsiz", "Ücretsiz (SQL Server'ın aksine lisans yok)"],
    ], [0.26, 0.37, 0.37]),
    ("p", "SQLite öğrenmek için harikaydı, ama e-ticaret aynı anda birçok kullanıcının sipariş verdiği bir sistem. "
          "Ayrıca geliştirmede de production'daki veritabanını kullanmak, sürprizleri önler."),
    ("h2", "pgAdmin"),
    ("p", "PostgreSQL için tarayıcıdan çalışan yönetim arayüzü. Tabloları görmek, SQL sorgusu çalıştırmak, "
          "migration'ların doğru uygulanıp uygulanmadığını kontrol etmek için kullanacağız. "
          "Adres: <font name='Mono'>http://localhost:5050</font>"),
    ("h2", "Mailpit ve SMTP"),
    ("p", "<b>SMTP</b> (Simple Mail Transfer Protocol), e-posta göndermek için kullanılan standart protokoldür. "
          "<b>Mailpit</b> sahte bir SMTP sunucusudur: uygulamanın gönderdiği mailleri gerçek adrese iletmez, yakalayıp "
          "kendi arayüzünde gösterir. Böylece test ederken yanlışlıkla gerçek kişilere mail atmayız. "
          "Uygulama maili <font name='Mono'>1025</font> portuna gönderir, biz <font name='Mono'>http://localhost:8025</font> "
          "adresinden okuruz. Production'da sadece SMTP adresini gerçek bir servise çevirmek yeterli olacak."),

    ("h2", "Port nedir? Neden 5433?"),
    ("p", "Bir bilgisayarda çalışan her ağ uygulaması bir <b>port numarası</b> dinler: aynı binadaki daire numaraları "
          "gibi. Bilgisayarında zaten kurulu bir PostgreSQL servisi 5432'yi (PostgreSQL'in varsayılan portu) "
          "kullanıyordu. İki program aynı portu dinleyemez, bu yüzden Docker'dakini <b>5433</b>'ten dışarı açtık."),
    ("table", [
        ["Port", "Servis"],
        ["3000", "React geliştirme sunucusu (Vite)"],
        ["5001", "ASP.NET Core API (HTTPS)"],
        ["5433", "PostgreSQL (Docker, bilgisayardan erişim)"],
        ["5050", "pgAdmin arayüzü"],
        ["8025 / 1025", "Mailpit arayüzü / SMTP"],
    ], [0.25, 0.75]),
    ("warn", "Karşılaştığımız tuzak: PostgreSQL 18 volume yolu",
     "PostgreSQL 18'den itibaren veri klasörü <font name='Mono'>/var/lib/postgresql/data</font> yerine "
     "<font name='Mono'>/var/lib/postgresql</font> oldu. İnternetteki eski örneklerin çoğu eski yolu kullanıyor; "
     "kopyalarsan container açılmaz. Ders: Örnek kod kopyalarken hangi sürüm için yazıldığına bak."),

    # ------------------------------------------------------------------
    ("h1", "9. Bu adımlarda ne yaptık?"),
    ("table", [
        ["Adım", "Yapılan", "Commit"],
        ["0", "Visual Studio 2026 ve .NET 11 SDK kuruldu, proje net11.0'a çevrildi, EF Core 11, "
              ".sln → .slnx, şablon dosyaları (WeatherForecast) silindi, .gitignore güncellendi.",
         "<font name='Mono'>aefd4dd</font>"],
        ["1", "docker-compose.yml ile PostgreSQL 18, pgAdmin, Mailpit kuruldu; şifreler .env'ye alındı, "
              ".env.example eklendi.",
         "<font name='Mono'>ba1f40a</font>"],
    ], [0.09, 0.73, 0.18]),

    ("h1", "10. Sözlük"),
    ("terms", [
        ("API", "Application Programming Interface. Programların birbiriyle konuşma kuralları. Bizde HTTP + JSON."),
        ("JSON", "Veri taşımak için kullanılan metin formatı: <font name='Mono'>{\"name\": \"Board\", \"price\": 20000}</font>."),
        ("Framework", "Uygulamanın iskeletini hazır sunan, kuralları belli büyük kütüphane (ASP.NET Core)."),
        ("ORM", "Nesneler ile veritabanı tabloları arasında çeviri yapan araç (EF Core)."),
        ("Migration", "Veritabanı şemasındaki değişikliğin kod olarak kaydı."),
        ("DI", "Dependency Injection. Bir sınıfın ihtiyaç duyduğu nesneleri dışarıdan alması."),
        ("Middleware", "İsteğin geçtiği sıralı ara katman (CORS, auth, hata yönetimi)."),
        ("CORS", "Farklı adresteki bir sayfanın API'ye erişmesine izin veren tarayıcı kuralı."),
        ("Image / Container", "Paket (kalıp) / o paketten çalışan kopya."),
        ("Volume", "Container silinse de kalan kalıcı veri alanı."),
        ("LTS / STS", "3 yıl / 2 yıl güvenlik desteği alan .NET sürümü."),
        ("SMTP", "E-posta gönderme protokolü."),
        ("Environment variable", "Programa dışarıdan verilen ayar değeri. Şifreler koda değil buraya yazılır."),
    ]),

    ("h1", "11. Kendini test et"),
    ("p", "Cevaplarını yüksek sesle ya da kâğıda yaz; zorlandığın soru olursa ilgili bölüme dön."),
    ("steps", [
        "SDK ile runtime arasındaki fark nedir? Sunucuya hangisini kurarsın?",
        ".NET 11 bir STS sürümü olduğu halde neden .NET 10 LTS yerine onu seçtik?",
        "Controller'ımız <font name='Mono'>StoreContext</font>'i neden <font name='Mono'>new</font> ile oluşturmuyor? Bunun faydası ne?",
        "EF Core'da migration ne işe yarar? Migration olmasaydı ne yapmak zorunda kalırdık?",
        "Fiyatı neden <font name='Mono'>decimal</font> 200.00 yerine <font name='Mono'>long</font> 20000 olarak tutuyoruz?",
        "Image ile container arasındaki fark nedir?",
        "<font name='Mono'>docker compose down</font> ile <font name='Mono'>docker compose down -v</font> arasındaki fark nedir? Hangisi tehlikeli?",
        "pgAdmin'den bağlanırken neden host'a <font name='Mono'>localhost</font> değil <font name='Mono'>postgres</font>, port'a 5433 değil 5432 yazdık?",
        "<font name='Mono'>.env</font> ile <font name='Mono'>.env.example</font>'ın farkı nedir? Hangisi GitHub'a gider?",
        "Mailpit kullanmasaydık test sırasında ne gibi bir risk olurdu?",
    ]),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "Adim-00-01-Ortam-ve-Altyapi.pdf")
    build(os.path.abspath(out),
          "Adım 0-1: Ortam ve Altyapı",
          ".NET 11 yükseltmesi, ASP.NET Core ve EF Core temelleri, Docker ile PostgreSQL, pgAdmin ve Mailpit",
          B, "E-Commerce Projesi · Ders Notları · Adım 0-1")
    print("ok", os.path.abspath(out))
