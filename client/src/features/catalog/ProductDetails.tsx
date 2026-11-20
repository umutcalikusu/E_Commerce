import { useParams } from "react-router";
import {
  Button,
  Divider,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useFetchProductDetailsQuery } from "./catalogApi";
import { formatCurrency } from "../../lib/util";

export default function ProductDetails() {
  const { id } = useParams();
  const { data: product, isLoading } = useFetchProductDetailsQuery(
    id ? +id : 0,
  );

  if (!product || isLoading) return <div>Yükleniyor...</div>;
  const productDetails = [
    { label: "İsim", value: product.name },
    { label: "Açıklama", value: product.description },
    { label: "Tür", value: product.type },
    { label: "Marka", value: product.brand },
    { label: "Stok Miktarı", value: product.quantityInStock },
  ];
  return (
    <Grid container spacing={6} sx={{ mx: "auto", maxWidth: "lg" }}>
      <Grid size={6}>
        <img
          src={product?.pictureUrl}
          alt={product.name}
          style={{ width: "100%" }}
        />
      </Grid>
      <Grid size={6}>
        <Typography variant="h3">{product.name}</Typography>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="h4" color="secondary">
          {formatCurrency(product.price)}
        </Typography>
        <TableContainer>
          <Table sx={{ "& td": { fontSize: "1rem" } }}>
            <TableBody>
              {productDetails.map((detail, index) => (
                <TableRow key={index}>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    {detail.label}
                  </TableCell>
                  <TableCell>{detail.value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Grid container spacing={2} sx={{ mt: 3 }}>
          <Grid size={6}>
            <TextField
              variant="outlined"
              type="number"
              label="Sepetteki adet"
              fullWidth
              defaultValue={1}
            />
          </Grid>
          <Grid size={6}>
            <Button
              color="primary"
              size="large"
              variant="contained"
              fullWidth
              sx={{ height: "55px" }}
            >
              Sepete Ekle
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}
