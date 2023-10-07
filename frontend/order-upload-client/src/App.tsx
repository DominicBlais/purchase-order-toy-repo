import React, { useEffect, useState } from 'react';
import { Button, Form, Input, Row, DatePicker, Layout, Upload, Table, message  } from 'antd';
import type { UploadProps } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';


const { Header, Footer, Sider, Content } = Layout;

type FieldType = {
  vendor_name?: string;
  order_date?: string;
  file?: File;
};

const fileProps: UploadProps = {
  name: 'file',
  beforeUpload: (file) => {
    return false;
  }
}

interface DataType {
  id: number;
  vendor_name: string;
  order_date: number;
  model_number: string;
  unit_price: number;
  quantity: number;
}

const columns: ColumnsType<DataType> = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    sorter: (a, b) => a.id - b.id
  },
  {
    title: 'Vendor Name',
    dataIndex: 'vendor_name',
    key: 'vendor_name',
    sorter: (a, b) => a.vendor_name.localeCompare(b.vendor_name)
  },
  {
    title: 'Order Date',
    dataIndex: 'order_date',
    key: 'order_date',
    render: (text) => <span>{new Date(text).toLocaleDateString()}</span>,
    sorter: (a, b) => a.order_date - b.order_date
  },
  {
    title: 'Model Number',
    dataIndex: 'model_number',
    key: 'model_number',
    sorter: (a, b) => a.model_number.localeCompare(b.model_number)
  },
  {
    title: 'Unit Price',
    dataIndex: 'unit_price',
    key: 'unit_price',
    render: (text) => <span>{"$" + text.toFixed(2)}</span>,
    sorter: (a, b) => a.unit_price - b.unit_price
  },
  {
    title: 'Quantity',
    dataIndex: 'quantity',
    key: 'quantity',
    sorter: (a, b) => a.quantity - b.quantity
  }
];

const App: React.FC = () => {
  const [data, setData] = useState<DataType[]>();
  
  const updateTable = async() => {
    const res = await fetch("http://127.0.0.1:8169/po/get_order_details", { method: "GET", mode: "cors"});
    const res_json = await res.json();
    if (res_json["status"] === "error") {
      message.error("An error occurred loading the existing purchase orders.");
    } else {
      var tableData: DataType[] = []
      for (var i = 0; i < res_json["details"].length; i++) {
        const row = res_json["details"][i];
        tableData.push({
          id: row["detail_id"],
          vendor_name: row["vendor_name"],
          order_date: row["order_date"],
          model_number: row["model_number"],
          unit_price: row["unit_price"],
          quantity: row["quantity"]
        })
      }
      setData(tableData);
    }
  };

  useEffect(() => {
    document.title = "Purchase Order Uploader";
    updateTable();
  }, []);
  
const onFinish = async (values: any) => {
  const formData = new FormData();
  formData.append("vendor_name", values["vendor_name"]);
  formData.append("order_date", "" + values["order_date"].valueOf());
  formData.append("file", values["file"].file);

  // todo: make this portable
  const res = await fetch("http://127.0.0.1:8169/po/upload_order_details", {
    method: "POST",
    mode: "cors",
    body: formData
  }); 
  const res_json = await res.json();
  if (res.status == 200) {
    if (res_json["status"] === "success") {
      message.success("Order details added!");
      updateTable();
    } else {
      message.error(res_json["message"]);
    } 
  } else {
    message.error("An unknown error occurred.")
  }
};

  const onFinishFailed = (errorInfo: any) => {
    message.error("An unknown error occurred.");
  };

  return (
  <Layout>
    <Header className="header">
      <h1>Purchase Order Uploader</h1>
    </Header>
    <Layout hasSider>
      <Sider width="350" className="sider" theme="light">

        <Row align="middle">
      <Form
        name="po_form"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600, margin:20 }}
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item<FieldType>
          label="Vendor Name"
          name="vendor_name"
          rules={[{ required: true, message: 'Please enter the vendor\'s name.' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item<FieldType>
          label="Order Date"
          name="order_date"
          rules={[{ required: true, message: 'Please choose an order date.' }]}
        >
          <DatePicker/>
        </Form.Item>

        <Form.Item<FieldType>
          label="CSV order file"
          name="file"
          rules={[{ required: true, message: 'Please select a CSV file.' }]}
        >
          <Upload {...fileProps}>
            <Button icon={<UploadOutlined />}>Select a File</Button>
          </Upload>
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form></Row>
      </Sider>
      <Content>
        <Table bordered columns={columns} dataSource={data} />
      </Content>
    </Layout>
    <Footer>
      Utilities &rarr; <a href="/po/reset_database">Clear Database</a> &bull; <a href="/shutdown">Shutdown Server</a>
    </Footer>

  </Layout>
)};

export default App;
