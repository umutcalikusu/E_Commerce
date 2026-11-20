using ECommerce.Application.Products;
using ECommerce.Application.Products.Interface;
using Microsoft.AspNetCore.Mvc;

namespace ECommerce.API.Controllers;

[Route("api/[controller]")]
[ApiController]
public class ProductsController(IProductService productService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<List<ProductDto>>> GetProducts(CancellationToken ct) =>
        await productService.GetProductsAsync(ct);

    [HttpGet("{id:int}")]
    public async Task<ActionResult<ProductDto>> GetProduct(int id, CancellationToken ct)
    {
        var product = await productService.GetProductAsync(id, ct);
        if (product is null) return NotFound();
        return product;
    }
}
