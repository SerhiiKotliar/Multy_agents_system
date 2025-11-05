import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import requests
import subprocess
import time


class OllamaClient:
    """Клієнт для роботи з локальною моделлю через Ollama"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3:8b"):
        self.base_url = base_url
        self.model = model
        self.available = False
        self._initialize_connection()

    def _initialize_connection(self):
        """Ініціалізація з'єднання з автоматичним запуском Ollama"""
        print("🔍 Перевірка доступності Ollama...")

        for url in ["http://localhost:11434", "http://127.0.0.1:11434"]:
            self.base_url = url
            if self._check_connection():
                self.available = True
                print(f"✅ Ollama знайдено за адресою: {url}")
                return

        print("❌ Ollama не знайдено.")

    def _check_connection(self) -> bool:
        """Перевірка з'єднання з Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                print(f"📋 Доступні моделі: {model_names}")

                # Пріоритет менших моделей для швидкості
                preferred_models = [
                    'llama3.2:1b', 'llama3.2:3b', 'llama3.2',
                    'llama3:8b', 'llama3:latest', 'llama3',
                    'gemma3:4b', 'gemma3:latest'
                ]

                for preferred in preferred_models:
                    for available_model in model_names:
                        if preferred in available_model:
                            self.model = available_model
                            print(f"🎯 Використовуємо модель: {self.model}")
                            return True

                # Якщо не знайшли пріоритетні, беремо першу доступну
                if model_names:
                    self.model = model_names[0]
                    print(f"🎯 Використовуємо першу доступну модель: {self.model}")
                    return True

                return False
        except Exception:
            return False

    def generate_response(self, messages: List[Dict], temperature: float = 0.7,
                          max_tokens: int = 500) -> str:  # Зменшимо токени
        """Генерація відповіді через Ollama API"""
        if not self.available:
            return "❌ Ollama не доступна."

        try:
            prompt = self._format_messages_optimized(messages)

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_k": 20,  # Обмежуємо для швидкості
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                }
            }

            print(f"🔄 Запит до {self.model}...")
            start_time = time.time()

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # Зменшимо таймаут
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
                return f"❌ Помилка API: {response.status_code}"

        except requests.exceptions.Timeout:
            return "❌ Таймаут. Спробуйте меншу модель або простіше питання."
        except Exception as e:
            return f"❌ Помилка: {str(e)}"

    def _format_messages_optimized(self, messages: List[Dict]) -> str:
        """Оптимізований формат для швидкої відповіді"""
        system_msg = ""
        user_msg = ""

        for message in messages:
            if message["role"] == "system":
                system_msg = message["content"][:500]  # Обмежуємо системні повідомлення
            elif message["role"] == "user":
                user_msg = message["content"]

        # Простий формат для швидкої обробки
        if system_msg:
            return f"Інструкція: {system_msg}\n\nПитання: {user_msg}\n\nВідповідь:"
        else:
            return f"Питання: {user_msg}\n\nВідповідь:"


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
            return "🤖 **Технічна підтримка:**\n\nДля детальних технічних консультацій рекомендується використовувати менші AI моделі або звернутися до технічної документації."
        elif any(word in question for word in billing_words):
            return "💼 **Фінансові питання:**\n\nДля обробки фінансових запитів використовуйте структуровані команди: 'рахунок', 'відшкодування', 'політика'."
        else:
            return "❓ **Питання не розпізнано**\n\nСпробуйте одне з цих питань:\n• Що таке IP-адреса?\n• Як працює Wi-Fi?\n• Створити рахунок\n• Політика відшкодувань"


class HybridAIClient:
    """Гібридний клієнт з пріоритетом на швидкість"""

    def __init__(self):
        print("🔄 Ініціалізація AI клієнтів...")

        self.ollama_client = OllamaClient()
        self.fast_client = FastLocalClient()

        self._print_status()

    def _print_status(self):
        """Вивід статусу"""
        print("\n📊 Статус AI клієнтів:")
        print(f"   • Ollama: {'✅' if self.ollama_client.available else '❌'}")
        if self.ollama_client.available:
            print(f"     Модель: {self.ollama_client.model}")
        print(f"   • Швидкий режим: ✅")

    def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Генерація відповіді з пріоритетом на швидкість"""
        # Спочатку швидкий локальний клієнт
        fast_response = self.fast_client.generate_response(messages)
        if not fast_response.startswith("❓"):
            return fast_response

        # Потім Ollama якщо доступна
        if self.ollama_client.available:
            print("🔄 Використання Ollama для детальної відповіді...")
            ollama_response = self.ollama_client.generate_response(messages, **kwargs)
            if not ollama_response.startswith("❌"):
                return f"🤖 **Детальна відповідь (AI):**\n\n{ollama_response}"

        return fast_response


# Решта класів залишаються незмінними (TechnicalAgentA, BillingAgentB, AgentDispatcher)
# [Вставте тут TechnicalAgentA, BillingAgentB, AgentDispatcher з попереднього коду]

class TechnicalAgentA:
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

    def search_documents(self, query: str, top_k: int = 2) -> List[Dict]:  # Зменшимо кількість
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
                    'content': doc['content'][:200],  # Обмежуємо довжину
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

        ai_response = self.ai_client.generate_response(messages, temperature=0.3, max_tokens=300)
        return f"{self.agent_name}:\n{ai_response}"


class BillingAgentB:
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

        ai_response = self.ai_client.generate_response(messages, temperature=0.5, max_tokens=300)
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
        response = f"{self.agent_name}:\n📋 **Політика відшкодувань**\n\n"
        for policy_type, details in self.refund_policy.items():
            response += f"**{details['description']}:** {details['days']} днів"
            if details['fee'] > 0:
                response += f" (комісія {details['fee'] * 100}%)"
            response += "\n"
        return response


class AgentDispatcher:
    def __init__(self, ai_client=None):
        self.agent_a = TechnicalAgentA("./docs", ai_client)
        self.agent_b = BillingAgentB(ai_client)
        self.ai_client = ai_client
        self.conversation_history = []

    def classify_intent(self, question: str) -> Tuple[str, float]:
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
    print("🚀 Запуск оптимізованої системи...")
    print("=" * 50)

    ai_client = HybridAIClient()
    dispatcher = AgentDispatcher(ai_client)

    print("\n💬 Система готова до роботи!")
    print("Доступні команди: статистика, історія, clear, quit, статус")
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