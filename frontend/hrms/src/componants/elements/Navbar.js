import React, {Component} from 'react';
import {Disclosure, DisclosureButton, DisclosurePanel} from "@headlessui/react";
import {Bars3Icon, XMarkIcon} from "@heroicons/react/24/outline";


function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}
export default function Navbar({navigation}){
    {
        return (
            <Disclosure as="nav" className="bg-gray-50">
                {({ open }) => (
                    <>
                        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8  md:flex md:flex-col md:items-center ">
                            <div className="flex h-16 items-center justify-between">
                                <div className="flex items-center">
                                    <div className="flex-shrink-0">
                                        <img
                                            className="h-8 w-8"
                                            src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                                            alt="Your Company"
                                        />
                                    </div>
                                    <div className="hidden md:block">
                                        <div className="ml-10 flex items-baseline space-x-4">
                                            {navigation.map((item) => (
                                                <a
                                                    key={item.name}
                                                    href={item.href}
                                                    className={ classNames(
                                                        item.current
                                                            ? ' text-purple-950 hover:text-purple-900 hover:bg-gray-150'
                                                            : 'text-purple-800 hover:bg-gray-100 hover:text-purple-900',
                                                        'rounded-md px-3 py-2 text-sm font-medium'
                                                    )}
                                                    aria-current={item.current ? 'page' : undefined}
                                                >
                                                    {item.name}
                                                </a>
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                <div className="-mr-2 flex md:hidden">
                                    {/* Mobile menu button */}
                                    <DisclosureButton className="relative inline-flex items-center justify-center rounded-md bg-gray-50 p-2 text-gray-700 hover:bg-gray-50  focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-100">
                                        <span className="absolute -inset-0.5" />
                                        <span className="sr-only">Open main menu</span>
                                        {open ? (
                                            <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                                        ) : (
                                            <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                                        )}
                                    </DisclosureButton>
                                </div>
                            </div>
                        </div>

                        <DisclosurePanel className="md:hidden">
                            <div className="space-y-1 px-2 pb-3 pt-2 sm:px-3">
                                {navigation.map((item) => (
                                    <DisclosureButton
                                        key={item.name}
                                        as="a"
                                        href={item.href}
                                        className={classNames(
                                            item.current ? ' text-purple-950 hover:text-purple-900 hover:bg-gray-150'
                                                : 'text-purple-800 hover:bg-gray-100 hover:text-purple-900',
                                            'block rounded-md px-3 py-2 text-base font-medium'
                                        )}
                                        aria-current={item.current ? 'page' : undefined}
                                    >
                                        {item.name}
                                    </DisclosureButton>
                                ))}
                            </div>
                        </DisclosurePanel>
                    </>
                )}
            </Disclosure>
        );
    }
}
