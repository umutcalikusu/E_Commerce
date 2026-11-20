using System;
using System.Collections.Generic;
using System.Text;

namespace ECommerce.Application.Products.Interface
{
    public interface IProductService
    {
        Task<List<ProductDto>> GetProductsAsync(CancellationToken ct = default);
        Task<ProductDto?> GetProductAsync(int id, CancellationToken ct = default);
    }
}
