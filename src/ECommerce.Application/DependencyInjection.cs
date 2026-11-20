using ECommerce.Application.Products.Interface;
using ECommerce.Application.Products.Service;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Text;

namespace ECommerce.Application
{
    public static class DependencyInjection
    {
        extension(IServiceCollection services)
        {
            public IServiceCollection AddApplication()
            {
                services.AddScoped<IProductService, ProductService>();
                return services;
            }
        }
    }
}
