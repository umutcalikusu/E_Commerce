using ECommerce.Application.Common.Interfaces;
using ECommerce.Application.Products.Interface;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Text;

namespace ECommerce.Application.Products.Service
{
    public class ProductService(IAppDbContext db) : IProductService
    {
        public Task<List<ProductDto>> GetProductsAsync(CancellationToken ct = default) =>
            db.Products.AsNoTracking()
                .Select(ProductMappings.ToDto)
                .ToListAsync(ct);

        public Task<ProductDto?> GetProductAsync(int id, CancellationToken ct = default) =>
            db.Products.AsNoTracking()
                .Where(p => p.Id == id)
                .Select(ProductMappings.ToDto)
                .FirstOrDefaultAsync(ct);
    }
}
