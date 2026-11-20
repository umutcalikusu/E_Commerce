"""Adım 2 ders notu: Clean Architecture ve PostgreSQL'e geçiş."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfkit import build  # noqa: E402

M = lambda s: f"<font name='Mono'>{s}</font>"  # noqa: E731

B = [
    ("note", "Bu adımda ne değişti?",
     "Uygulama dışarıdan aynı görünüyor: aynı 18 ürün, aynı adresler, React hiç değişmedi. Ama içeride tek "
     "parça bir projeden <b>4 katmanlı</b> bir yapıya geçtik ve veritabanı SQLite dosyasından Docker'daki "
     "<b>PostgreSQL</b>'e taşındı. Bu tür \"dışarıdan görünmeyen ama içeriyi düzelten\" değişikliğe "
     "<b>refactoring</b> denir."),

    # ------------------------------------------------------------------
    ("h1", "1. Neden mimari değiştirdik?"),
    ("p", "Eski yapıda controller doğrudan " + M("StoreContext") + "'i kullanıyordu. 2 endpoint için sorun yok. "
          "Ama proje büyüdükçe (sepet, sipariş, ödeme, kupon, admin...) şu sorunlar çıkar:"),
    ("bullets", [
        "<b>Her şey her şeye bağlı olur.</b> Ödeme kodu controller'da, indirim hesabı başka bir controller'da, "
        "aynı mantık üç yerde kopyalanmış olur.",
        "<b>Değiştirmek korkutucu hale gelir.</b> iyzico'yu başka bir ödeme sağlayıcıyla değiştirmek, "
        "onlarca dosyaya dokunmak demektir.",
        "<b>Test yazmak zorlaşır.</b> İş kuralını test etmek için gerçek veritabanı ve gerçek ödeme servisi gerekir.",
    ]),
    ("p", "Clean Architecture bu sorunları, kodu <b>sorumluluklarına göre katmanlara</b> ayırarak ve katmanlar "
          "arasındaki bağımlılığa <b>tek bir yön</b> vererek çözer."),

    # ------------------------------------------------------------------
    ("h1", "2. Clean Architecture"),
    ("p", "Robert C. Martin (\"Uncle Bob\") tarafından popülerleştirilen bir mimari yaklaşım. Temel fikir: "
          "<b>iş kuralları merkezdedir</b>, veritabanı, web, ödeme sistemi gibi teknik detaylar dışarıdadır ve "
          "merkeze bağımlıdır. Merkez dışarıyı tanımaz."),
    ("flow", [
        ("API", "Controller'lar<br/>Program.cs"),
        ("Application", "Servisler, DTO'lar<br/>Interface'ler"),
        ("Domain", "Entity'ler<br/>İş kuralları"),
    ]),
    ("p", "Infrastructure ise yandan bağlanır: Application'daki interface'leri <b>uygular</b> "
          "(implement eder). API, uygulama açılırken ikisini birbirine bağlar."),
    ("table", [
        ["Katman", "Sorumluluğu", "Bizde ne var", "Bağımlı olduğu"],
        ["<b>Domain</b>", "İşin kendisi. Teknolojiden bağımsız kurallar.", M("Product") + " entity'si",
         "Hiçbiri"],
        ["<b>Application</b>", "Kullanım senaryoları: \"ürünleri listele\", \"sipariş oluştur\".",
         M("IProductService") + ", " + M("ProductService") + ", " + M("ProductDto") + ", " + M("IAppDbContext"),
         "Domain"],
        ["<b>Infrastructure</b>", "Dış dünyayla konuşan teknik kod.",
         M("StoreContext") + ", Npgsql, migration'lar, seed. İleride iyzico, Cloudinary, e-posta.",
         "Application"],
        ["<b>API</b>", "HTTP isteklerini karşılar, her şeyi birbirine bağlar.",
         M("ProductsController") + ", " + M("Program.cs"), "Application, Infrastructure"],
    ], [0.17, 0.30, 0.35, 0.18]),
    ("tip", "Altın kural: Bağımlılıklar içeri doğru",
     "Domain projesinin csproj dosyasına bak: hiçbir referansı yok. Application, PostgreSQL'i ya da Npgsql'i "
     "tanımıyor; sadece " + M("IAppDbContext") + " interface'ini biliyor. Yarın PostgreSQL yerine SQL Server "
     "kullanmak istesek <b>sadece Infrastructure</b> değişir, Application ve Domain'e dokunmayız."),

    ("h2", "Dependency Inversion: Application veritabanını nasıl kullanıyor?"),
    ("p", "Application veritabanına ihtiyaç duyuyor ama Infrastructure'a referansı yok (ok ters yönde olurdu). "
          "Çözüm: Application ihtiyacını bir <b>interface</b> olarak tanımlar, Infrastructure bu interface'i uygular. "
          "Buna SOLID prensiplerinin \"D\"si, <b>Dependency Inversion</b> denir."),
    ("code", """// Application: "Bana Products'ı olan ve kaydedebilen bir şey lazım"
public interface IAppDbContext
{
    DbSet<Product> Products { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}

// Infrastructure: "Ben o şeyim"
public class StoreContext(...) : DbContext(options), IAppDbContext

// Infrastructure DI kaydı: "IAppDbContext isteyene StoreContext'i ver"
services.AddScoped<IAppDbContext>(sp => sp.GetRequiredService<StoreContext>());"""),
    ("note", "Pragmatik bir tercih",
     "Saf Clean Architecture'da Application, EF Core'u (" + M("DbSet") + ") bile tanımamalıdır. Biz bilinçli "
     "olarak Application'a EF Core paketini ekledik. Böylece her entity için ayrı repository sınıfı yazmaktan "
     "kurtulduk. Bu yaklaşım sektörde yaygın (Jason Taylor'ın Clean Architecture şablonu da böyle) ve bu boyutta "
     "bir proje için doğru denge."),

    ("h2", "Bilinçli olarak kullanmadıklarımız"),
    ("table", [
        ["Araç", "Ne işe yarar", "Neden yok"],
        ["<b>MediatR</b>", "Controller ile servis arasına mesajlaşma katmanı koyar (CQRS).",
         "2025'te ticari lisansa geçti. Ayrıca bu ölçekte doğrudan servis çağırmak daha anlaşılır."],
        ["<b>AutoMapper</b>", "Entity'yi DTO'ya otomatik çevirir.",
         "Ticari lisansa geçti. Elle mapping daha hızlı, hataları derleme anında yakalanır."],
        ["<b>Generic Repository</b>", M("IRepository&lt;T&gt;") + " ile her tabloya ortak CRUD.",
         "EF Core'un " + M("DbSet") + "'i zaten bir repository. Üstüne bir katman daha eklemek fayda getirmiyor."],
    ], [0.20, 0.38, 0.42]),

    # ------------------------------------------------------------------
    ("h1", "3. Solution yapısı ve ortak dosyalar"),
    ("code", """E_Commerce/
├── global.json                  ← hangi SDK kullanılacak
├── Directory.Build.props        ← tüm projelere ortak ayarlar
├── Directory.Packages.props     ← tüm paket sürümleri tek yerde
├── E_Commerce.slnx
├── docker-compose.yml
├── src/
│   ├── ECommerce.Domain/
│   ├── ECommerce.Application/
│   ├── ECommerce.Infrastructure/
│   └── ECommerce.API/
└── client/                      ← React"""),
    ("terms", [
        ("classlib", M("dotnet new classlib") + " bir <b>sınıf kütüphanesi</b> oluşturur: tek başına çalışmayan, "
                     "başka projelerin kullandığı kod paketi (.dll). Domain, Application ve Infrastructure böyle. "
                     "Çalışan tek proje API."),
        ("ProjectReference", "Bir projenin başka bir projeyi kullanabilmesi için verilen izin. "
                             + M("dotnet add X reference Y") + " ile eklenir. Mimarideki oklar bunlar."),
        ("global.json", "Projenin hangi .NET SDK sürümüyle derleneceğini sabitler. "
                        + M("rollForward: latestFeature") + " → 11.0.1xx serisinin en yenisini kullanabilir."),
        ("Directory.Build.props", "MSBuild, her projeyi derlerken bu dosyayı <b>bulunduğu klasörden yukarı doğru</b> "
                                  "arar ve içindeki ayarları projeye ekler. " + M("TargetFramework") + ", "
                                  + M("Nullable") + " gibi ayarları 4 kere yazmıyoruz."),
        ("Central Package Management", M("Directory.Packages.props") + " içinde " + M("ManagePackageVersionsCentrally") +
         " açılınca paket sürümleri sadece orada yazılır, csproj'larda " + M("Version") + " olmaz. Faydası: "
         "Application ve Infrastructure aynı EF Core sürümünü kullanmak <b>zorunda</b>. Npgsql 11 çıkınca tek satır değişecek."),
    ]),
    ("warn", "Karşılaştığımız hata: NU1008 ve yanlış klasör",
     "Komutlar repo yerine bir üst klasörde çalıştığı için " + M("Directory.Packages.props") + " de üst klasöre "
     "oluştu. MSBuild props dosyasını yukarı doğru aradığı için eski " + M("API.csproj") + " onu buldu; eski "
     "csproj'da " + M("Version=") + " yazdığı için \"PackageReference items cannot define a value for Version\" "
     "hatası çıktı. Üstelik dosyalar git reposunun dışında kalmıştı. Ders: Komut çalıştırmadan önce "
     + M("pwd") + " ile nerede olduğuna bak."),
    ("warn", "Karşılaştığımız tuzak: Boş klasör görünmüyor",
     "Visual Studio boş klasörleri Solution Explorer'da göstermez. " + M("Controllers") + " klasörü diskte vardı "
     "ama boştu; aynı isimle yenisi oluşturulamadı. Çözüm: Solution Explorer'da <b>Show All Files</b>."),

    # ------------------------------------------------------------------
    ("h1", "4. Application katmanındaki kavramlar"),
    ("h2", "DTO (Data Transfer Object)"),
    ("p", "API'nin dışarıya döndürdüğü veri modeli. Entity'yi <b>asla doğrudan dışarı vermiyoruz</b>, çünkü:"),
    ("bullets", [
        "<b>Güvenlik:</b> İleride " + M("User") + " entity'sinde şifre hash'i olacak. Entity'yi döndürseydik "
        "o da JSON'a girerdi.",
        "<b>Bağımsızlık:</b> Veritabanında kolon adı değişse bile API'nin cevabı (React'ın beklediği şekil) aynı kalır.",
        "<b>Döngü sorunu:</b> " + M("Order → OrderItems → Order") + " gibi ilişkiler JSON'a çevrilirken sonsuz döngüye girebilir.",
    ]),
    ("code", """public record ProductDto(int Id, string Name, string Description, long Price,
    string PictureUrl, string Type, string Brand, int QuantityInStock);"""),
    ("p", "<b>record</b>, veri taşımak için tasarlanmış özel bir sınıf türüdür. Tek satırda constructor ve "
          "property'ler oluşur, değerleri sonradan değiştirilemez (immutable) ve iki record içerikleri aynıysa "
          "eşit sayılır. DTO için ideal."),

    ("h2", "Mapping ve Expression"),
    ("p", "Entity'yi DTO'ya çevirmeye <b>mapping</b> denir. Bunu sıradan bir metot yerine "
          + M("Expression&lt;Func&lt;Product, ProductDto&gt;&gt;") + " olarak yazdık. Farkı önemli:"),
    ("table", [
        ["", M("Func&lt;Product, ProductDto&gt;"), M("Expression&lt;Func&lt;...&gt;&gt;")],
        ["Nedir", "Derlenmiş, çalıştırılabilir kod", "Kodun <b>tarifi</b> (ağaç yapısında veri)"],
        ["EF Core ne yapabilir", "İçine bakamaz, sadece çalıştırır", "İçini okuyup <b>SQL'e çevirebilir</b>"],
        ["Sonuç", "Tüm kolonlar çekilir, çeviri bellekte yapılır", "Sadece DTO'da gereken kolonlar SELECT edilir"],
    ], [0.22, 0.39, 0.39]),
    ("p", M(".Select(ProductMappings.ToDto)") + " yazdığımızda EF Core ifadeyi okuyup "
          + M("SELECT \"Id\", \"Name\", ... FROM \"Products\"") + " üretir. Buna <b>projection</b> denir. "
          "İleride DTO'da 3 alan olan bir listeleme yaptığımızda 30 kolonluk tablonun hepsi çekilmeyecek."),

    ("h2", "AsNoTracking"),
    ("p", "EF Core normalde okuduğu her nesneyi <b>takip eder</b> (change tracking): değişiklik yaparsan "
          + M("SaveChanges") + " neyi güncelleyeceğini bilsin diye. Sadece okuyup ekrana göstereceğimiz veride "
          "bu takip boşa bellek ve zaman harcar. " + M("AsNoTracking()") + " takibi kapatır. Kural: "
          "<b>Sadece okuma yapan sorgularda AsNoTracking kullan.</b>"),

    ("h2", "CancellationToken"),
    ("p", "Kullanıcı sayfayı kapatırsa ya da isteği iptal ederse ASP.NET Core bunu bir " + M("CancellationToken") +
          " ile bildirir. Bu token'ı controller'dan servise, oradan EF Core'a kadar taşıdık; böylece iptal edilen "
          "bir isteğin veritabanı sorgusu da yarıda kesilir ve sunucu boşuna çalışmaz."),

    # ------------------------------------------------------------------
    ("h1", "5. Dependency Injection: servis kayıtları"),
    ("p", "Her katman kendi servislerini kendi " + M("DependencyInjection.cs") + " dosyasında kaydediyor. "
          "Program.cs sadece ikisini çağırıyor:"),
    ("code", """builder.Services
    .AddApplication()                          // Application kendi servislerini kaydeder
    .AddInfrastructure(builder.Configuration); // Infrastructure veritabanını kaydeder"""),
    ("h2", "Servis ömürleri (lifetime)"),
    ("table", [
        ["Ömür", "Ne zaman yeni nesne oluşur", "Ne için"],
        ["<b>Transient</b>", "Her istendiğinde", "Hafif, durumsuz yardımcı sınıflar"],
        ["<b>Scoped</b>", "Her HTTP isteği için bir tane", "DbContext ve onu kullanan servisler (bizimkiler)"],
        ["<b>Singleton</b>", "Uygulama boyunca tek bir tane", "Ayarlar, önbellek, HTTP client fabrikası"],
    ], [0.18, 0.37, 0.45]),
    ("p", M("AddDbContext") + " DbContext'i <b>Scoped</b> kaydeder. " + M("ProductService") + " DbContext kullandığı "
          "için onu da " + M("AddScoped") + " ile kaydettik. Kural: Bir servis, kendisinden <b>daha kısa</b> ömürlü "
          "bir servise bağımlı olmamalı (Singleton içinde Scoped kullanmak hatadır)."),

    ("h2", "Yeni C# 14 özelliği: extension blokları"),
    ("p", M("AddApplication()") + " aslında " + M("IServiceCollection") + "'a dışarıdan eklenmiş bir metot "
          "(extension method). C# 14 bunun için yeni ve daha düzenli bir sözdizimi getirdi:"),
    ("code", """// Eski yazım (hâlâ geçerli)
public static IServiceCollection AddApplication(this IServiceCollection services) { ... }

// Yeni C# 14 yazımı: aynı tipe ait birden çok extension tek blokta toplanır
extension(IServiceCollection services)
{
    public IServiceCollection AddApplication() { ... }
}"""),
    ("p", "Yeni yazımın asıl gücü, extension <b>property</b> ve statik üye de tanımlayabilmesi. Eski yazımla sadece metot eklenebiliyordu."),

    # ------------------------------------------------------------------
    ("h1", "6. Infrastructure: EF Core + PostgreSQL"),
    ("h2", "Npgsql"),
    ("p", "<b>Npgsql</b>, .NET için PostgreSQL sürücüsüdür. " + M("Npgsql.EntityFrameworkCore.PostgreSQL") +
          " paketi ise EF Core'un PostgreSQL ile konuşmasını sağlayan <b>provider</b>'dır. SQLite'tan geçişte "
          "tek fark " + M("UseSqlite(...)") + " yerine " + M("UseNpgsql(...)") + " yazmak oldu; gerisi aynı. "
          "ORM kullanmanın faydası tam olarak bu."),
    ("warn", "Sürüm kararı: Neden EF Core 10?",
     "EF Core 11 çıkmıştı ama Npgsql 11 sadece RC (Release Candidate, test sürümü) durumundaydı. Kararlı "
     "EF Core 11'i test sürümü bir sürücüyle karıştırmak çalışma anında hata riski taşır. Kararlı "
     "<b>EF Core 10 + Npgsql 10</b> çifti .NET 11 üzerinde sorunsuz çalışıyor. Npgsql 11 çıkınca "
     + M("Directory.Packages.props") + "'ta sürümleri değiştirmek yeterli. Ders: Paketlerin <b>birbiriyle uyumlu</b> "
     "sürümlerini seç; \"en yeni\" her zaman doğru cevap değil."),

    ("h2", "Fluent API ve IEntityTypeConfiguration"),
    ("p", "Tablo kurallarını (kolon uzunluğu, index, ilişkiler) iki yerde yazabilirsin: entity üstüne attribute "
          "olarak (" + M("[MaxLength(200)]") + ") ya da ayrı bir konfigürasyon sınıfında (<b>Fluent API</b>). "
          "Fluent API'yi seçtik, çünkü attribute kullansaydık Domain'in EF Core'a bağımlı olması gerekirdi."),
    ("code", """public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.Property(p => p.Name).HasMaxLength(200);   // → character varying(200)
    }
}

// StoreContext: bu assembly'deki TÜM configuration sınıflarını otomatik bul ve uygula
modelBuilder.ApplyConfigurationsFromAssembly(typeof(StoreContext).Assembly);"""),
    ("p", "Sonuç pgAdmin'de görünüyor: " + M("Name") + " kolonu artık " + M("character varying(200)") + ". "
          "Sınırsız metin yerine sınır koymak, hem veritabanını hem de kötü niyetli dev girdileri kontrol altında tutar."),

    ("h2", "UseSeeding ve UseAsyncSeeding (EF Core 9+)"),
    ("p", "Eskiden ayrı bir " + M("DbInitializer") + " sınıfını Program.cs'ten elle çağırıyorduk. EF Core 9 ile gelen "
          "bu özellikle seed mantığı DbContext ayarlarının içinde duruyor ve <b>migration uygulandıktan sonra "
          "otomatik çalışıyor</b>. İki versiyon yazmamızın sebebi:"),
    ("bullets", [
        M("MigrateAsync()") + " (uygulama açılışı) → " + M("UseAsyncSeeding") + " çağrılır.",
        M("dotnet ef database update") + " (komut satırı) → " + M("UseSeeding") + " çağrılır.",
    ]),
    ("p", "İkisinde de önce " + M("Any()") + " ile tabloyu kontrol ediyoruz; böylece uygulama her açıldığında ürünler "
          "tekrar tekrar eklenmiyor. Bu özelliğe <b>idempotent</b> denir: kaç kere çalışırsa çalışsın sonuç aynı."),

    ("h2", "Migration: yeniden başlangıç"),
    ("code", """dotnet ef migrations add InitialCreate -p src/ECommerce.Infrastructure -s src/ECommerce.API -o Persistence/Migrations"""),
    ("terms", [
        (M("-p") + " (project)", "Migration dosyalarının yazılacağı proje: DbContext'in olduğu Infrastructure."),
        (M("-s") + " (startup)", "Ayarların (connection string, DI) okunacağı çalışan proje: API."),
        (M("-o") + " (output)", "Dosyaların konacağı klasör."),
        ("__EFMigrationsHistory", "EF Core'un veritabanında tuttuğu tablo. Hangi migration'ların uygulandığını "
                                  "kaydeder; " + M("MigrateAsync") + " sadece eksik olanları çalıştırır."),
    ]),
    ("p", "Eski SQLite migration'larını taşımadık, sildik. Her veritabanı motorunun SQL'i farklıdır (SQLite'ta "
          + M("INTEGER") + ", PostgreSQL'de " + M("integer generated by default as identity") + "). Henüz gerçek veri "
          "olmadığı için PostgreSQL için temiz bir " + M("InitialCreate") + " ile başlamak en doğrusu."),

    # ------------------------------------------------------------------
    ("h1", "7. Gizli bilgiler: user-secrets"),
    ("p", "Connection string içinde veritabanı şifresi var. Bunu " + M("appsettings.json") + "'a yazarsak "
          "GitHub'a gider. ASP.NET Core'un <b>user-secrets</b> özelliği, geliştirme ortamındaki gizli ayarları "
          "proje klasörünün <b>dışında</b>, Windows kullanıcı klasöründe saklar:"),
    ("code", """%APPDATA%\\Microsoft\\UserSecrets\\<UserSecretsId>\\secrets.json"""),
    ("p", M("dotnet user-secrets init") + " csproj'a bir " + M("UserSecretsId") + " ekler; ASP.NET Core geliştirme "
          "ortamında bu dosyayı otomatik okur."),
    ("h2", "Ayarlar nereden okunuyor? (Configuration öncelik sırası)"),
    ("table", [
        ["Sıra", "Kaynak", "Ne için"],
        ["1 (en zayıf)", M("appsettings.json"), "Herkese açık, varsayılan ayarlar. Git'e gider."],
        ["2", M("appsettings.Development.json"), "Geliştirme ortamına özel, şifresiz ayarlar. Git'e gider."],
        ["3", "User secrets", "Geliştirmede şifreler. Git'e gitmez. Sadece Development ortamında okunur."],
        ["4", "Environment variables", "Production'da şifreler (sunucu ya da Docker ortam değişkeni)."],
        ["5 (en güçlü)", "Komut satırı argümanları", "Anlık geçersiz kılma."],
    ], [0.16, 0.33, 0.51]),
    ("p", "Aynı anahtar birden çok yerde varsa <b>sonraki kazanır</b>. " + M("GetConnectionString(\"DefaultConnection\")") +
          " aslında " + M("ConnectionStrings:DefaultConnection") + " anahtarını bu katmanlarda arıyor. Bu yüzden "
          + M(".gitignore") + "'daki " + M("API/appsettings.json") + " satırını kaldırdık: artık o dosyada sır yok, "
          "commit'lenmesi gerekiyor."),

    # ------------------------------------------------------------------
    ("h1", "8. API katmanı"),
    ("h2", "Controller artık ince"),
    ("code", """public class ProductsController(IProductService productService) : ControllerBase
{
    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> GetProduct(int id, CancellationToken ct)
    {
        var product = await productService.GetProductAsync(id, ct);
        if (product is null) return NotFound();
        return product;
    }
}"""),
    ("bullets", [
        "<b>İnce controller (thin controller):</b> Controller'ın tek işi HTTP ile servis arasında tercümanlık. "
        "Sorgu ya da iş kuralı yok.",
        "<b>Route constraint:</b> " + M("{id:int}") + " → " + M("/api/products/abc") + " isteği metoda hiç gelmez, "
        "doğrudan 404 döner.",
        "<b>ActionResult&lt;T&gt;:</b> Hem " + M("ProductDto") + " hem de " + M("NotFound()") + " döndürebilmemizi sağlar.",
    ]),
    ("h2", "OpenAPI"),
    ("p", "<b>OpenAPI</b>, bir API'nin hangi endpoint'leri olduğunu, ne aldığını ve ne döndürdüğünü tarif eden "
          "standart bir formattır (eski adıyla Swagger). " + M("AddOpenApi()") + " ve " + M("MapOpenApi()") +
          " ile .NET bu dokümanı otomatik üretiyor: " + M("https://localhost:5001/openapi/v1.json") + ". Adım 4'te "
          "buna <b>Scalar</b> arayüzünü ekleyip API'yi tarayıcıdan test edilebilir hale getireceğiz."),
    ("h2", "Açılışta otomatik migration"),
    ("p", "Program.cs geliştirme ortamında açılırken " + M("MigrateAsync()") + " çağırıyor: eksik migration'lar "
          "uygulanıyor, ardından seed çalışıyor. Projeyi klonlayan biri sadece " + M("docker compose up") + " ve "
          + M("dotnet run") + " ile hazır veritabanına sahip oluyor. (Production'da bu yöntem riskli; migration'lar "
          "orada kontrollü şekilde ayrıca uygulanır.)"),
    ("warn", "Karşılaştığımız hata: Connection refused",
     "\"Failed to connect to 127.0.0.1:5433 ... hedef makine etkin olarak reddetti\": Docker Desktop kapalıydı, "
     "o portu dinleyen bir program yoktu. Ders: Bağlantı hatasında sırayla kontrol et: "
     "<b>1)</b> Servis çalışıyor mu? (" + M("docker compose ps") + ") <b>2)</b> Port doğru mu? "
     "<b>3)</b> Kullanıcı adı ve şifre doğru mu? Şifre yanlış olsaydı mesaj "
     + M("password authentication failed") + " olurdu."),

    # ------------------------------------------------------------------
    ("h1", "9. Bu adımda ne yaptık?"),
    ("steps", [
        M("global.json") + ", " + M("Directory.Build.props") + " ve " + M("Directory.Packages.props") + " eklendi.",
        "4 proje oluşturuldu, solution'a eklendi, referanslar mimariye göre kuruldu.",
        M("Product") + " Domain'e taşındı.",
        "Application: " + M("IAppDbContext") + ", " + M("ProductDto") + ", " + M("ProductMappings") + ", "
        + M("IProductService") + " / " + M("ProductService") + ", DI kaydı.",
        "Infrastructure: " + M("StoreContext") + ", " + M("ProductConfiguration") + ", " + M("ProductSeed") +
        ", Npgsql, " + M("UseSeeding") + ".",
        "API: Servis kullanan " + M("ProductsController") + ", yeni Program.cs, port 5001, user-secrets.",
        "Eski " + M("API/") + " projesi ve SQLite kaldırıldı, PostgreSQL için " + M("InitialCreate") + " migration'ı oluşturuldu.",
        "Doğrulama: 18 ürün PostgreSQL'de, " + M("/api/products") + " çalışıyor, olmayan ürün 404 dönüyor, React katalog sayfası çalışıyor.",
    ]),

    ("h1", "10. Sözlük"),
    ("terms", [
        ("Refactoring", "Davranışı değiştirmeden kodun iç yapısını iyileştirmek."),
        ("Katman (layer)", "Belli bir sorumluluğu olan, diğerlerinden ayrılmış kod grubu."),
        ("Dependency Inversion", "Üst seviye kodun somut sınıfa değil interface'e bağımlı olması."),
        ("Interface", "Bir sınıfın \"neler yapabileceğinin\" sözleşmesi; nasıl yaptığını söylemez."),
        ("DTO", "Katmanlar ya da sistemler arasında veri taşıyan, davranışı olmayan basit model."),
        ("record", "Değeri değiştirilemeyen, içerik bazlı eşitliği olan veri tipi."),
        ("Projection", "Sorguda tüm entity yerine sadece gereken alanları seçmek (" + M("Select") + ")."),
        ("Expression tree", "Kodun çalıştırılabilir hali yerine veri olarak tutulan tarifi; EF Core bunu SQL'e çevirir."),
        ("Change tracking", "EF Core'un okuduğu nesnelerdeki değişiklikleri izlemesi."),
        ("Lifetime", "DI'da bir servis nesnesinin ne kadar yaşadığı: Transient, Scoped, Singleton."),
        ("Provider", "EF Core'un belirli bir veritabanıyla konuşmasını sağlayan paket (Npgsql)."),
        ("Fluent API", "Tablo kurallarını zincirleme metotlarla ayrı bir sınıfta tanımlama yöntemi."),
        ("Idempotent", "Kaç kere çalıştırılırsa çalıştırılsın aynı sonucu veren işlem."),
        ("User secrets", "Geliştirmede şifreleri proje dışında saklayan ASP.NET Core özelliği."),
        ("OpenAPI", "API'nin endpoint'lerini tarif eden standart doküman formatı."),
        ("RC", "Release Candidate: Kararlı sürümden hemen önceki test sürümü."),
    ]),

    ("h1", "11. Kendini test et"),
    ("steps", [
        "Domain projesinin neden hiçbir projeye referansı yok? Olsaydı ne kaybederdik?",
        "Application, PostgreSQL'i tanımadığı halde ürünleri veritabanından nasıl okuyabiliyor?",
        "iyzico yerine PayTR kullanmak istesek hangi katman(lar) değişirdi?",
        "Entity yerine neden DTO döndürüyoruz? En az iki sebep say.",
        M("Func") + " yerine " + M("Expression") + " kullanmamız veritabanı sorgusunu nasıl etkiliyor?",
        M("AsNoTracking()") + "'i ne zaman kullanırsın, ne zaman kullanmazsın?",
        "DbContext neden Scoped? Singleton olsaydı ne gibi bir sorun çıkardı?",
        "Central Package Management olmadan Application ve Infrastructure farklı EF Core sürümleri kullansa ne olurdu?",
        "Neden EF Core 11 yerine EF Core 10 seçtik?",
        "Connection string'deki şifre nerede duruyor? Uygulama onu nasıl buluyor?",
        M("UseSeeding") + " içinde " + M("Any()") + " kontrolü olmasaydı ne olurdu?",
        "\"Connection refused\" ile \"password authentication failed\" hataları sana ne söyler?",
    ]),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "Adim-02-Clean-Architecture-ve-PostgreSQL.pdf")
    build(os.path.abspath(out),
          "Adım 2: Clean Architecture ve PostgreSQL",
          "Katmanlı mimari, DTO ve mapping, Dependency Injection, EF Core + Npgsql, Fluent API, seeding, user-secrets",
          B, "E-Commerce Projesi · Ders Notları · Adım 2")
    print("ok", os.path.abspath(out))
