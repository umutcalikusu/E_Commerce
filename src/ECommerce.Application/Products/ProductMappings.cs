using ECommerce.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Text;

namespace ECommerce.Application.Products
{
    public static class ProductMappings
    {
        public static readonly Expression<Func<Product, ProductDto>> ToDto = p =>
       new ProductDto(p.Id, p.Name, p.Description, p.Price,
           p.PictureUrl, p.Type, p.Brand, p.QuantityInStock);
    }
}
