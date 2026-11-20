using System;
using System.Collections.Generic;
using System.Text;

namespace ECommerce.Application.Products
{
    public record ProductDto(int Id, string Name, string Description, long Price,
        string PictureUrl, string Type, string Brand, int QuantityInStock);
}
