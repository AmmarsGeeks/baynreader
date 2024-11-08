window.addEventListener('load', function() {
    const invoices = JSON.parse(localStorage.getItem('invoices')) || [];
    const invoiceTableBody = document.getElementById('invoice-table').querySelector('tbody');
    let totalAmount = 0; // متغير لحفظ المجموع الكلي
    const addedProducts = {}; // كائن لتتبع المنتجات المضافة

    // إضافة بيانات الفواتير الجديدة (إذا كان لديك بيانات جديدة ترغب في إضافتها)
    const newInvoices = [
        {
            description: "مطهر أرضيات برائحة اللافندر 7 لتر",
            quantity: 1,
            price: 52.90,
            taxable: 46.00,
            vat: 6.90,
            total: 52.90
        },
        {
            description: "صابونة بودي برائحة اللافندر 6 لتر",
            quantity: 1,
            price: 52.90,
            taxable: 46.00,
            vat: 6.90,
            total: 52.90
        },
        {
            description: "ملح زجاج عرض 1+1 لاأثاث المعالج 6",
            quantity: 1,
            price: 35.01,
            taxable: 30.44,
            vat: 4.57,
            total: 35.01
        },
        {
            description: "سيروم جل صنفور 12 كيلوا لاأثاث المعالج",
            quantity: 1,
            price: 55.20,
            taxable: 48.00,
            vat: 7.20,
            total: 55.20
        },
        {
            description: "سيروم جل صنفور 6 كيلوا لاأثاث المعالج",
            quantity: 1,
            price: 55.20,
            taxable: 48.00,
            vat: 7.20,
            total: 55.20
        }
    ];

    // دمج بيانات الفواتير الجديدة مع الفواتير الحالية
    invoices.push(...newInvoices);

    // إضافة كل فاتورة إلى الجدول
    invoices.forEach(invoice => {
        // تحقق من القيم إذا كانت تساوي صفر
        if (invoice.quantity > 0 && invoice.price > 0 && invoice.taxable > 0 && invoice.vat > 0 && invoice.total > 0) {
            // تحقق من المنتج المتكرر
            if (!addedProducts[invoice.description]) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${invoice.description}</td>
                    <td>${invoice.quantity}</td>
                    <td>${invoice.price.toFixed(2)}</td>
                    <td>${invoice.taxable.toFixed(2)}</td>
                    <td>${invoice.vat.toFixed(2)}</td>
                    <td>${invoice.total.toFixed(2)}</td>
                `;
                invoiceTableBody.appendChild(row); // إضافة الصف إلى الجدول

                // إضافة المجموع لكل فاتورة
                totalAmount += invoice.total; // إضافة المجموع لكل فاتورة

                // إضافة المنتج إلى الكائن لتتبع المضافات
                addedProducts[invoice.description] = true;
            }
        }
    });

    // عرض المجموع الكلي
    document.getElementById('total-sum').innerText = totalAmount.toFixed(2); // تحديث المجموع في الخلية
});

// إضافة حدث زر "إرسال الفاتورة"
document.getElementById('submit-invoice').addEventListener('click', function() {
    const fileInput = document.getElementById('invoice-file');

    // تحقق من وجود ملف
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];

        // استخدام FileReader لقراءة الصورة
        const reader = new FileReader();
        reader.onload = function(e) {
            // حفظ مسار الصورة في localStorage
            localStorage.setItem('lastUploadedInvoice', e.target.result);
            // متابعة عملية التعرف على النص باستخدام Tesseract.js (كما في السابق)
            // ...
        };
        reader.readAsDataURL(file); // قراءة الصورة كـ Base64
    } else {
        alert("يرجى اختيار ملف.");
    }
});
