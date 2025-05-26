#include <torch/torch.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QComboBox>
#include <QPushButton>
#include <QMessageBox>

using json = nlohmann::json;

const int LATENT_DIM = 3;

struct AutoEncoderImpl : torch::nn::Module {
    torch::nn::Linear enc{nullptr};
    torch::nn::Linear dec{nullptr};
    AutoEncoderImpl(int input_dim, int latent_dim=LATENT_DIM) {
        enc = register_module("enc", torch::nn::Linear(input_dim, latent_dim));
        dec = register_module("dec", torch::nn::Linear(latent_dim, input_dim));
    }
    torch::Tensor forward(torch::Tensor x) {
        auto h = torch::relu(enc->forward(x));
        return dec->forward(h);
    }
    torch::Tensor encode(torch::Tensor x) {
        return torch::relu(enc->forward(x));
    }
};
TORCH_MODULE(AutoEncoder);

struct Encodings {
    std::map<std::string,int> soldier_id;
    std::map<std::string,int> purpose;
    std::map<std::string,int> destination;
    std::map<std::string,int> time_slot;
    float threshold;
};

Encodings load_encodings(const std::string& path) {
    std::ifstream f(path);
    json j; f >> j;
    Encodings e;
    e.soldier_id = j["soldier_id"].get<std::map<std::string,int>>();
    e.purpose = j["purpose"].get<std::map<std::string,int>>();
    e.destination = j["destination"].get<std::map<std::string,int>>();
    e.time_slot = j["time_slot"].get<std::map<std::string,int>>();
    e.threshold = j["threshold"].get<float>();
    return e;
}

class App : public QWidget {
    Q_OBJECT
    AutoEncoder model;
    Encodings enc;
    torch::Tensor prev;
    QLineEdit *sidEdit;
    QComboBox *purposeBox;
    QComboBox *destBox;
    QComboBox *timeBox;
public:
    App(AutoEncoder m, Encodings e, QWidget *parent=nullptr)
        : QWidget(parent), model(m), enc(e), prev(torch::zeros({LATENT_DIM})) {
        auto *layout = new QVBoxLayout(this);
        layout->addWidget(new QLabel("군번"));
        sidEdit = new QLineEdit(this);
        layout->addWidget(sidEdit);
        layout->addWidget(new QLabel("방문 목적"));
        purposeBox = new QComboBox(this);
        for (auto &p : enc.purpose) purposeBox->addItem(QString::fromStdString(p.first));
        layout->addWidget(purposeBox);
        layout->addWidget(new QLabel("행선지"));
        destBox = new QComboBox(this);
        for (auto &d : enc.destination) destBox->addItem(QString::fromStdString(d.first));
        layout->addWidget(destBox);
        layout->addWidget(new QLabel("시간"));
        timeBox = new QComboBox(this);
        for (auto &t : enc.time_slot) timeBox->addItem(QString::fromStdString(t.first));
        layout->addWidget(timeBox);
        auto *btn = new QPushButton("확인", this);
        layout->addWidget(btn);
        connect(btn, &QPushButton::clicked, this, &App::check);
    }
private slots:
    void check() {
        std::string sid = sidEdit->text().toStdString();
        if (!enc.soldier_id.count(sid)) {
            QMessageBox::warning(this, "오류", "등록되지 않은 군번입니다");
            return;
        }
        auto sid_v = enc.soldier_id[sid];
        auto purpose_v = enc.purpose[purposeBox->currentText().toStdString()];
        auto dest_v = enc.destination[destBox->currentText().toStdString()];
        auto time_v = enc.time_slot[timeBox->currentText().toStdString()];
        torch::Tensor feat = torch::tensor({(float)sid_v,(float)purpose_v,(float)dest_v,(float)time_v});
        torch::Tensor x = torch::cat({prev, feat});
        torch::NoGradGuard no_grad;
        auto recon = model->forward(x);
        auto mse = torch::mse_loss(recon, x).item<float>();
        prev = model->encode(x).detach();
        if (mse > enc.threshold) {
            QMessageBox::information(this, "결과", QString("이상 출입! 오류="+QString::number(mse)));
        } else {
            QMessageBox::information(this, "결과", QString("정상 출입. 오류="+QString::number(mse)));
        }
    }
};

#include "access_control_gui.moc"

int main(int argc, char* argv[]) {
    Encodings enc = load_encodings("../encoding.json");
    int input_dim = 4 + LATENT_DIM;
    AutoEncoder model(input_dim);
    torch::load(model, "../model.pth");
    model->eval();

    QApplication app(argc, argv);
    App w(model, enc);
    w.show();
    return app.exec();
}

