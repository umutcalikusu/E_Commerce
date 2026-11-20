using ECommerce.Application.Common.Interfaces;
using ECommerce.Infrastructure.Persistence;
using ECommerce.Infrastructure.Persistence.Seed;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Text;

namespace ECommerce.Infrastructure
{
    public static class DependencyInjection
    {
        extension(IServiceCollection services)
        {
            public IServiceCollection AddInfrastructure(IConfiguration configuration)
            {
                var connectionString = configuration.GetConnectionString("DefaultConnection")
                    ?? throw new InvalidOperationException("'DefaultConnection' bulunamadı.");

                services.AddDbContext<StoreContext>(options => options
                    .UseNpgsql(connectionString)
                    .UseSeeding((context, _) =>
                    {
                        var db = (StoreContext)context;
                        if (db.Products.Any()) return;
                        db.Products.AddRange(ProductSeed.Products());
                        db.SaveChanges();
                    })
                    .UseAsyncSeeding(async (context, _, ct) =>
                    {
                        var db = (StoreContext)context;
                        if (await db.Products.AnyAsync(ct)) return;
                        db.Products.AddRange(ProductSeed.Products());
                        await db.SaveChangesAsync(ct);
                    }));

                services.AddScoped<IAppDbContext>(sp => sp.GetRequiredService<StoreContext>());
                return services;
            }
        }
    }
}
