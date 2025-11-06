import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import requests
import time
import os


class CloudAIClient:
    """Клієнт для роботи з хмарними моделями через Ollama"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.selected_model = None
        self.available = False
        self._initialize_connection()

    def _initialize_connection(self):
        """Ініціалізація з'єднання з Ollama"""
        print("🔍 Перевірка доступності Ollama та хмарних моделей...")

        if self._check_connection():
            self.available = True
            print(f"✅ Ollama знайдено за адресою: {self.base_url}")
            self._select_cloud_model()
        else:
            print("❌ Ollama не знайдено.")

    def _check_connection(self) -> bool:
        """Перевірка з'єднання з Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                self.available_models = [model['name'] for model in models]
                print(f"📋 Доступні моделі: {self.available_models}")
                return True
        except Exception as e:
            print(f"⚠️ Помилка підключення: {e}")
        return False

    def _select_cloud_model(self):
        """Вибір хмарної моделі з пріоритетом"""
        cloud_models = [
            'minimax-m2:cloud',
            'deepseek-v3.1:671b-cloud',
            'deepseek-coder-v2:16b-cloud',
            'qwen2.5:72b-cloud',
            'llama3.1:70b-cloud'
        ]

        for cloud_model in cloud_models:
            if cloud_model in self.available_models:
                self.selected_model = cloud_model
                print(f"🎯 Використовуємо хмарну модель: {self.selected_model}")
                return

        # Якщо хмарних моделей немає, шукаємо локальні
        local_models = ['llama3:8b', 'llama3.2:3b', 'gemma2:2b']
        for local_model in local_models:
            for available_model in self.available_models:
                if local_model in available_model:
                    self.selected_model = available_model
                    print(f"🎯 Використовуємо локальну модель: {self.selected_model}")
                    return

        # Якщо нічого не знайдено, беремо першу доступну
        if self.available_models:
            self.selected_model = self.available_models[0]
            print(f"🎯 Використовуємо першу доступну модель: {self.selected_model}")

    def generate_response(self, messages: List[Dict], temperature: float = 0.7,
                          max_tokens: int = 1000) -> str:
        """Генерація відповіді через хмарну модель"""
        if not self.available or not self.selected_model:
            return "❌ Жодна модель не доступна."

        try:
            prompt = self._format_messages_for_cloud(messages)

            payload = {
                "model": self.selected_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }

            print(f"🔄 Запит до {self.selected_model}...")
            start_time = time.time()

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # Більший таймаут для хмарних моделей
            )

            elapsed_time = time.time() - start_time
            print(f"⏱️ Час відповіді: {elapsed_time:.1f}с")

            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                if response_text:
                    return response_text
                else:
                    return "❌ Пуста відповідь від моделі."
            else:
                error_msg = f"❌ Помилка API: {response.status_code}"
                try:
                    error_detail = response.json().get('error', '')
                    if error_detail:
                        error_msg += f" - {error_detail}"
                except:
                    pass
                return error_msg

        except requests.exceptions.Timeout:
            return "❌ Таймаут запиту. Хмарна модель може бути перевантажена."
        except Exception as e:
            return f"❌ Помилка: {str(e)}"

    def _format_messages_for_cloud(self, messages: List[Dict]) -> str:
        """Форматує повідомлення для хмарних моделей"""
        formatted_text = ""

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                formatted_text += f"### Системна інструкція:\n{content}\n\n"
            elif role == "user":
                formatted_text += f"### Запит користувача:\n{content}\n\n"
            elif role == "assistant":
                formatted_text += f"### Попередня відповідь:\n{content}\n\n"

        formatted_text += "### Поточна відповідь:\n"
        return formatted_text

    def switch_model(self, model_name: str) -> bool:
        """Перемикання на іншу модель"""
        if model_name in self.available_models:
            self.selected_model = model_name
            print(f"🔄 Переключено на модель: {model_name}")
            return True
        else:
            print(f"❌ Модель {model_name} не знайдена")
            return False

    def get_available_cloud_models(self) -> List[str]:
        """Отримати список доступних хмарних моделей"""
        cloud_models = []
        for model in self.available_models:
            if ':cloud' in model or 'minimax' in model or 'deepseek' in model:
                cloud_models.append(model)
        return cloud_models


class FastLocalClient:
    """Швидкий локальний клієнт для миттєвих відповідей"""

    def __init__(self):
        self.available = True
        self.responses = {
            'ip': "🌐 **IP-адреса (Internet Protocol)** - це унікальна числова адреса, яка ідентифікує пристрій в мережі. IP-адреси використовуються для комунікації між пристроями в інтернеті та локальних мережах.\n\n**Типи IP-адрес:**\n• IPv4: 192.168.1.1 (32 біти)\n• IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 (128 біт)\n\n**Види:**\n• Публічні - для інтернету\n• Приватні - для локальних мереж\n• Статичні - постійні\n• Динамічні - що змінюються",

            'wifi': "📡 **Wi-Fi** - це технологія бездротового мережевого зв'язку, що дозволяє пристроям підключатися до інтернету та локальної мережі без кабелів.\n\n**Основні характеристики:**\n• Стандарти: 802.11a/b/g/n/ac/ax\n• Частоти: 2.4 GHz та 5 GHz\n• Безпекові протоколи: WEP, WPA, WPA2, WPA3",

            'компьютер': "💻 **Комп'ютер** - це електронний пристрій для обробки інформації. Основні компоненти:\n• Процесор (CPU) - мозок комп'ютера\n• Оперативна пам'ять (RAM) - тимчасова пам'ять\n• Жорсткий диск (HDD/SSD) - постійне сховище\n• Материнська плата - основна плата\n• Блок живлення - забезпечує енергією",

            'мережа': "🔗 **Мережа** - це система взаємопов'язаних пристроїв для обміну інформацією. Типи мереж:\n• LAN (Local Area Network) - локальна\n• WAN (Wide Area Network) - глобальна\n• WLAN (Wireless LAN) - бездротова\n• VPN (Virtual Private Network) - віртуальна приватна",

            'драйвер': "⚙️ **Драйвер** - це програмне забезпечення, яке дозволяє операційній системі взаємодіяти з апаратним забезпеченням. Без драйверів пристрої не працюватимуть коректно.",

            'рахунок': "🧾 **Рахунок/Інвойс** - це документ, що містить інформацію про послуги або товари та їх вартість. Для створення рахунку напишіть 'створити рахунок'.",

            'відшкодування': "💰 **Відшкодування** - це повернення коштів за послуги або товари. Типи відшкодувань:\n• Стандартне - 14 днів\n• Преміум - 7 днів\n• Експрес - 3 дні (комісія 10%)"
        }

    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Миттєва відповідь на основі шаблонів"""
        user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                user_message = msg["content"].lower()
                break

        # Пошук найбільш відповідного шаблону
        for keyword, response in self.responses.items():
            if keyword in user_message:
                return f"🤖 **Швидка відповідь:**\n\n{response}"

        return self._get_fallback_response(user_message)

    def _get_fallback_response(self, question: str) -> str:
        """Запасна відповідь"""
        tech_words = ['ip', 'wifi', 'network', 'computer', 'драйвер', 'мереж', 'компьютер']
        billing_words = ['рахунок', 'відшкодування', 'оплата', 'invoice', 'payment', 'refund']

        if any(word in question for word in tech_words):
            return "🤖 **Технічна підтримка:**\n\nДля детальних технічних консультацій використовується хмарна AI модель."
        elif any(word in question for word in billing_words):
            return "💼 **Фінансові питання:**\n\nДля обробки фінансових запитів використовуйте структуровані команди: 'рахунок', 'відшкодування', 'політика'."
        else:
            return "❓ **Питання не розпізнано**\n\nСпробуйте одне з цих питань:\n• Що таке IP-адреса?\n• Як працює Wi-Fi?\n• Створити рахунок\n• Політика відшкодувань"


class HybridAIClient:
    """Гібридний клієнт з пріоритетом на хмарні моделі"""

    def __init__(self):
        print("🔄 Ініціалізація AI клієнтів...")

        self.cloud_client = CloudAIClient()
        self.fast_client = FastLocalClient()

        self._print_status()

    def _print_status(self):
        """Вивід статусу"""
        print("\n📊 Статус AI клієнтів:")
        print(f"   • Хмарні моделі: {'✅' if self.cloud_client.available else '❌'}")
        if self.cloud_client.available and self.cloud_client.selected_model:
            model_type = "🌩️ Хмарна" if ":cloud" in self.cloud_client.selected_model else "💻 Локальна"
            print(f"     Модель: {self.cloud_client.selected_model} ({model_type})")

            cloud_models = self.cloud_client.get_available_cloud_models()
            if cloud_models:
                print(f"     Доступні хмарні моделі: {', '.join(cloud_models)}")

        print(f"   • Швидкий режим: ✅")

    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Генерація відповіді з пріоритетом на швидкість"""
        # Спочатку швидкий локальний клієнт
        fast_response = self.fast_client.generate_response(messages)
        if not fast_response.startswith("❓"):
            return fast_response

        # Потім хмарна модель якщо доступна
        if self.cloud_client.available:
            print(f"🔄 Використання {self.cloud_client.selected_model} для детальної відповіді...")
            cloud_response = self.cloud_client.generate_response(messages, **kwargs)
            if not cloud_response.startswith("❌"):
                model_type = "хмарної моделі" if ":cloud" in self.cloud_client.selected_model else "локальної моделі"
                return f"🤖 **Детальна відповідь ({model_type}):**\n\n{cloud_response}"

        return fast_response

    def switch_model(self, model_name: str) -> bool:
        """Перемикання моделі"""
        if self.cloud_client.available:
            return self.cloud_client.switch_model(model_name)
        return False

    def get_available_models(self) -> List[str]:
        """Отримати список доступних моделей"""
        if self.cloud_client.available:
            return self.cloud_client.available_models
        return []

class TechnicalAgentA:
    """Технічний агент"""
    def __init__(self, docs_directory: str = "./docs", ai_client=None):
        self.docs_directory = Path(docs_directory)
        self.documents = []
        self.ai_client = ai_client
        self.agent_name = "🤖 Агент А (Технічний спеціаліст)"
        self.load_documents()

    def load_documents(self):
        """Завантаження технічних документів"""
        try:
            text_files = list(self.docs_directory.glob("*.txt"))
            for file_path in text_files:
                content = file_path.read_text(encoding='utf-8')
                self.process_document(content, file_path.name)
        except Exception as e:
            print(f"❌ Помилка завантаження документів: {e}")

    def process_document(self, content: str, source: str):
        """Обробка документів"""
        sections = re.split(r'\n\s*\n', content)
        for i, section in enumerate(sections):
            if len(section.strip()) > 50:
                self.documents.append({
                    'content': section.strip(),
                    'source': source,
                    'section_id': i + 1
                })

    def search_documents(self, query: str, top_k: int = 2) -> List[Dict]:
        """Пошук релевантних документів"""
        if not self.documents:
            return []

        query_lower = query.lower()
        scored_docs = []

        for doc in self.documents:
            score = 0
            content_lower = doc['content'].lower()

            if query_lower in content_lower:
                score += 5

            query_words = query_lower.split()
            word_matches = sum(1 for word in query_words if len(word) > 3 and word in content_lower)
            score += word_matches

            if score > 0:
                scored_docs.append({
                    'content': doc['content'][:200],
                    'source': doc['source'],
                    'section_id': doc['section_id'],
                    'score': score
                })

        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]

    def handle_query(self, question: str) -> str:
        """Обробка запиту з використанням AI"""
        relevant_docs = self.search_documents(question)

        # Формуємо контекст для AI
        context = ""
        for doc in relevant_docs:
            context += f"\n--- {doc['source']} ---\n{doc['content']}\n"

        messages = [
            {
                "role": "system",
                "content": "Ти - технічний спеціаліст. Давай короткі точні відповіді українською."
            },
            {
                "role": "user",
                "content": f"Контекст:{context}\n\nПитання: {question}"
            }
        ]

        ai_response = self.ai_client.generate_response(messages, temperature=0.3, max_tokens=1000)
        return f"{self.agent_name}:\n{ai_response}"


class BillingAgentB:
    """Фінансовий агент"""
    def __init__(self, ai_client=None):
        self.agent_name = "💼 Агент Б (Спеціаліст з рахунків)"
        self.ai_client = ai_client
        self.refund_requests = {}
        self.invoices = {}
        self.refund_policy = {
            "standard": {"days": 14, "fee": 0.0, "description": "Стандартне відшкодування"},
            "premium": {"days": 7, "fee": 0.0, "description": "Преміум відшкодування"},
            "express": {"days": 3, "fee": 0.1, "description": "Експрес відшкодування (комісія 10%)"}
        }

    def handle_query(self, question: str) -> str:
        """Обробка запиту з використанням AI"""
        question_lower = question.lower()

        # Спочатку спробуємо обробити структурованими методами
        structured_response = self._try_structured_handling(question)
        if structured_response:
            return structured_response

        # Використовуємо AI
        messages = [
            {
                "role": "system",
                "content": "Ти - фахівець з рахунків. Давай короткі чіткі відповіді українською."
            },
            {
                "role": "user",
                "content": question
            }
        ]

        ai_response = self.ai_client.generate_response(messages, temperature=0.5, max_tokens=800)
        return f"{self.agent_name}:\n{ai_response}"

    def _try_structured_handling(self, question: str) -> Optional[str]:
        """Спробувати обробити запит структурованими методами"""
        question_lower = question.lower()

        if any(word in question_lower for word in ['відшкодування', 'рефанд', 'повернення', 'refund']):
            return self.handle_refund_request(question)
        elif any(word in question_lower for word in ['рахунок', 'інвойс', 'invoice', 'bill']):
            return self.handle_invoice_request(question)
        elif any(word in question_lower for word in ['політика', 'умови', 'терміни', 'policy']):
            return self.explain_refund_policy()

        return None

    def handle_refund_request(self, question: str) -> str:
        """запит на відшкодування"""
        request_id = f"REF-{uuid.uuid4().hex[:6].upper()}"
        refund_type = "standard"

        if "преміум" in question.lower():
            refund_type = "premium"
        elif "експрес" in question.lower():
            refund_type = "express"

        self.refund_requests[request_id] = {
            "type": refund_type,
            "status": "pending",
            "created_at": datetime.now()
        }

        return f"""{self.agent_name}:
✅ **Запит на відшкодування створено!**

📋 **Деталі {request_id}:**
• Тип: {self.refund_policy[refund_type]['description']}
• Термін: {self.refund_policy[refund_type]['days']} днів
• Комісія: {self.refund_policy[refund_type]['fee'] * 100}%

📝 **Наступні кроки:**
1. Заповніть форму на сайті
2. Надішліть документи
3. Чекайте підтвердження"""

    def handle_invoice_request(self, question: str) -> str:
        """запит на виставлення рахунку"""
        invoice_id = f"INV-{uuid.uuid4().hex[:6].upper()}"
        self.invoices[invoice_id] = {
            "amount": "1,000.00",
            "status": "generated",
            "created_at": datetime.now()
        }

        return f"""{self.agent_name}:
📄 **Рахунок {invoice_id} готовий!**

💳 **Оплата:**
• Онлайн: https://pay.company.com/{invoice_id}
• Банк: IBAN UA12 3456 7890 1234 5678 9012 345
• Термін: 30 днів"""

    def explain_refund_policy(self) -> str:
        """пояснення політики відшкодувань"""
        response = f"{self.agent_name}:\n📋 **Політика відшкодувань**\n\n"
        for policy_type, details in self.refund_policy.items():
            response += f"**{details['description']}:** {details['days']} днів"
            if details['fee'] > 0:
                response += f" (комісія {details['fee'] * 100}%)"
            response += "\n"
        return response


class AgentDispatcher:
    """агент диспетчера"""
    def __init__(self, ai_client=None):
        self.agent_a = TechnicalAgentA("./docs", ai_client)
        self.agent_b = BillingAgentB(ai_client)
        self.ai_client = ai_client
        self.conversation_history = []

    def classify_intent(self, question: str) -> Tuple[str, float]:
        """класифікація повідомлень"""
        tech_keywords = ['компьютер', 'ноутбук', 'мережа', 'інтернет', 'wi-fi', 'ip', 'mac', 'драйвер', 'software',
                         'hardware']
        billing_keywords = ['рахунок', 'інвойс', 'оплата', 'відшкодування', 'рефанд', 'гроші', 'кошти', 'ціна']

        question_lower = question.lower()
        tech_score = sum(1 for word in tech_keywords if word in question_lower)
        billing_score = sum(1 for word in billing_keywords if word in question_lower)

        if tech_score > billing_score:
            return "technical", 0.8
        elif billing_score > tech_score:
            return "billing", 0.8
        else:
            return "technical", 0.5

    def handle_message(self, user_message: str) -> str:
        """обробка повідомлення"""
        if not user_message.strip():
            return "Будь ласка, введіть ваше питання."

        intent, confidence = self.classify_intent(user_message)

        if intent == "technical":
            response = self.agent_a.handle_query(user_message)
        else:
            response = self.agent_b.handle_query(user_message)

        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user_message": user_message,
            "agent_response": response,
            "agent": intent
        })

        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        return response

    def get_conversation_stats(self) -> Dict:
        """отримання статистики"""
        agent_counts = {"technical": 0, "billing": 0}
        for entry in self.conversation_history:
            if entry["agent"] in agent_counts:
                agent_counts[entry["agent"]] += 1

        return {
            "total_messages": len(self.conversation_history),
            "agent_usage": agent_counts,
            "ai_available": self.ai_client is not None
        }


def main():
    print("🚀 Запуск системи з підтримкою хмарних моделей...")
    print("=" * 50)

    ai_client = HybridAIClient()
    dispatcher = AgentDispatcher(ai_client)

    print("\n💬 Система готова до роботи!")
    print("Доступні команди:")
    print("  - статистика - показати статистику розмови")
    print("  - моделі - показати доступні моделі")
    print("  - перемкнути <назва> - змінити модель")
    print("  - clear - очистити історію")
    print("  - quit - вихід")
    print("\nЗадавайте ваші питання:")

    while True:
        try:
            user_input = input("\n👤 Ваше повідомлення: ").strip()

            if user_input.lower() in ['quit', 'exit', 'вихід']:
                print("Бувайте здорові, дорогенькі!")
                break
            elif user_input.lower() == 'статистика':
                stats = dispatcher.get_conversation_stats()
                print(f"\n📊 Статистика: {stats['total_messages']} повідомлень")
                print(f"   • Технічні: {stats['agent_usage']['technical']}")
                print(f"   • Фінансові: {stats['agent_usage']['billing']}")
                continue
            elif user_input.lower() == 'моделі':
                models = ai_client.get_available_models()
                if models:
                    print(f"\n📋 Доступні моделі:")
                    for model in models:
                        model_type = "🌩️ Хмарна" if ":cloud" in model else "💻 Локальна"
                        print(f"   • {model} ({model_type})")
                else:
                    print("❌ Моделі не знайдено")
                continue
            elif user_input.lower().startswith('перемкнути'):
                model_name = user_input[10:].strip()
                if model_name:
                    if ai_client.switch_model(model_name):
                        print(f"✅ Переключено на модель: {model_name}")
                    else:
                        print(f"❌ Не вдалося перемкнути на модель: {model_name}")
                continue
            elif user_input.lower() == 'clear':
                dispatcher.conversation_history = []
                print("🗑️ Історія очищена!")
                continue

            response = dispatcher.handle_message(user_input)
            print(f"\n{response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Помилка: {e}")


if __name__ == "__main__":
    docs_dir = Path("./docs")
    docs_dir.mkdir(exist_ok=True)
    main()