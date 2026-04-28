/* =========================================================
   App JS - Sistema de Tienda
   Funciona tanto si la app está montada en `/` como en `/api/`
   porque usa rutas relativas a la página actual.
   ========================================================= */

// Base relativa. Si la página actual es `.../inventario_view`,
// las llamadas a `inventario` van a `.../inventario`.
function api(path) {
  // path empieza sin slash
  return path;
}

async function jsonFetch(url, opts = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { detail: text }; }
  if (!res.ok) throw new Error(data.detail || res.statusText);
  return data;
}

/* ================= Inventario ================== */
const InventarioPage = {
  async init() {
    document.getElementById("btnRecargar")
      .addEventListener("click", () => this.cargar());
    document.getElementById("filtro")
      .addEventListener("input", (e) => this.filtrar(e.target.value));
    await this.cargar();
  },

  async cargar() {
    try {
      const data = await jsonFetch(api("inventario"));
      this._datos = data.productos || [];
      this.render(this._datos);
    } catch (e) {
      document.getElementById("tbody").innerHTML =
        `<tr><td colspan="7" class="msg error">${e.message}</td></tr>`;
    }
  },

  filtrar(q) {
    q = q.toLowerCase();
    const filtrados = (this._datos || []).filter(p =>
      p.nombre.toLowerCase().includes(q) ||
      (p.categoria || "").toLowerCase().includes(q)
    );
    this.render(filtrados);
  },

  render(productos) {
    const tbody = document.getElementById("tbody");
    if (!productos.length) {
      tbody.innerHTML = `<tr><td colspan="7">Sin productos</td></tr>`;
      return;
    }
    tbody.innerHTML = productos.map(p => `
      <tr>
        <td>${p.id_producto}</td>
        <td>${escapeHtml(p.nombre)}</td>
        <td>${escapeHtml(p.categoria || "")}</td>
        <td>${p.codigo_barras ?? ""}</td>
        <td>$${Number(p.precio_venta).toFixed(2)}</td>
        <td>${p.stock} ${p.stock < 5 ? '<span class="badge low">bajo</span>' : ""}</td>
        <td>
          <button class="danger" data-id="${p.id_producto}" data-act="del">Eliminar</button>
        </td>
      </tr>
    `).join("");
    tbody.querySelectorAll("button[data-act=del]").forEach(btn => {
      btn.addEventListener("click", () => this.eliminar(btn.dataset.id));
    });
  },

  async eliminar(id) {
    if (!confirm("¿Eliminar producto " + id + "?")) return;
    try {
      await jsonFetch(api("inventario/" + id), { method: "DELETE" });
      this.cargar();
    } catch (e) { alert(e.message); }
  },
};

/* ================= Agregar ================== */
const AgregarPage = {
  init() {
    document.getElementById("form")
      .addEventListener("submit", (e) => this.submit(e));
  },
  async submit(e) {
    e.preventDefault();
    const msg = document.getElementById("msg");
    msg.className = "msg"; msg.textContent = "";
    const data = {
      tipo:           document.getElementById("tipo").value,
      id:             parseInt(document.getElementById("id").value),
      nombre:         document.getElementById("nombre").value.trim(),
      categoria:      document.getElementById("categoria").value,
      codigo_barras:  parseInt(document.getElementById("codigo").value),
      precio_compra:  parseFloat(document.getElementById("compra").value),
      precio_venta:   parseFloat(document.getElementById("venta").value),
      stock:          parseFloat(document.getElementById("stock").value),
    };
    try {
      const r = await jsonFetch(api("inventario/agregar"), {
        method: "POST", body: JSON.stringify(data),
      });
      msg.textContent = `${r.mensaje} (id final: ${r.id_producto})`;
      e.target.reset();
    } catch (err) {
      msg.className = "msg error";
      msg.textContent = err.message;
    }
  },
};

/* ================= Venta ================== */
const VentaPage = {
  carrito: [],

  async init() {
    await this.cargarProductos();
    document.getElementById("btnAdd").addEventListener("click", () => this.add());
    document.getElementById("btnCobrar").addEventListener("click", () => this.cobrar());
  },

  async cargarProductos() {
    const data = await jsonFetch(api("inventario"));
    const sel = document.getElementById("selProducto");
    sel.innerHTML = data.productos.map(p =>
      `<option value="${p.id_producto}" data-nombre="${escapeAttr(p.nombre)}"
               data-precio="${p.precio_venta}" data-stock="${p.stock}">
         ${p.nombre} - $${p.precio_venta} (stock ${p.stock})
       </option>`).join("");
  },

  add() {
    const sel = document.getElementById("selProducto");
    const opt = sel.options[sel.selectedIndex];
    if (!opt) return;
    const cant = parseFloat(document.getElementById("cant").value);
    if (!cant || cant <= 0) return alert("Cantidad invalida");

    this.carrito.push({
      id: parseInt(sel.value),
      nombre: opt.dataset.nombre,
      precio: parseFloat(opt.dataset.precio),
      cantidad: cant,
    });
    this.render();
  },

  render() {
    const tb = document.getElementById("carrito");
    tb.innerHTML = this.carrito.map((it, i) => `
      <tr>
        <td>${it.id}</td>
        <td>${escapeHtml(it.nombre)}</td>
        <td>${it.cantidad}</td>
        <td>$${it.precio.toFixed(2)}</td>
        <td>$${(it.precio * it.cantidad).toFixed(2)}</td>
        <td><button class="danger" data-i="${i}">Quitar</button></td>
      </tr>
    `).join("");
    tb.querySelectorAll("button[data-i]").forEach(b =>
      b.addEventListener("click", () => {
        this.carrito.splice(parseInt(b.dataset.i), 1);
        this.render();
      })
    );
  },

  async cobrar() {
    if (!this.carrito.length) return alert("Carrito vacío");

    const body = {
      items: this.carrito.map(it => ({
        id_producto: it.id, cantidad: it.cantidad,
      })),
    };

    const cliId  = document.getElementById("cliId").value;
    const cliNom = document.getElementById("cliNombre").value.trim();
    const cliTel = document.getElementById("cliTel").value.trim();
    if (cliId && cliNom) {
      body.cliente = { id: parseInt(cliId), nombre: cliNom, telefono: cliTel };
    }

    const dt = document.getElementById("descTipo").value;
    const dv = parseFloat(document.getElementById("descVal").value);
    if (dt && dv > 0) {
      body.descuentos = [{ tipo: dt, valor: dv }];
    }

    try {
      const r = await jsonFetch(api("venta"), {
        method: "POST", body: JSON.stringify(body),
      });
      document.getElementById("ticket").textContent = r.ticket;
      this.carrito = [];
      this.render();
      this.cargarProductos();
    } catch (e) {
      alert(e.message);
    }
  },
};

/* utils */
function escapeHtml(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function escapeAttr(s) { return escapeHtml(s); }
