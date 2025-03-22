import { Container } from "@mui/material";
import ProductList from "./ProductList";
import { Product } from "../../app/models/product";

type Props = {
  products: Product[];
};
export default function Catalog({ products }: Props) {
  return (
    <Container>
      <ProductList products={products} />
    </Container>
  );
}
